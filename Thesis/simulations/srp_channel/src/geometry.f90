!> Rectangular SRP open-channel geometry.
!>
!> The physical passage is nonperiodic in x and bounded by stationary walls in
!> y and z.  The underlying grid is periodic in y and z because the NGA2 FFT
!> pressure solver requires those directions to be periodic; immersed-boundary
!> walls separate the physical passage from the added periodic padding cells.
module geometry
   use ibconfig_class, only: ibconfig
   use precision,      only: WP
   implicit none
   private

   type(ibconfig), public :: cfg

   public :: geometry_init

contains

   subroutine geometry_init
      use param,       only: param_read,param_exists
      use sgrid_class, only: sgrid,cartesian
      implicit none
      type(sgrid) :: grid
      integer :: i,j,k,l,m,nx,ny,nz,npad,n_rods,n_sheets
      real(WP) :: Lx,Ly,Lz,dy,dz,Ly_grid,Lz_grid
      real(WP) :: rod_diameter,rod_thickness,rod_span,sheet_x,stack_center_x,sheet_spacing
      real(WP) :: separator_thickness,separator_depth,separator_y,divider_gib
      real(WP) :: divider_ylo,divider_yhi,divider_height
      character(len=32) :: porous_geometry
      real(WP), dimension(:), allocatable :: x,y,z

      ! Lx, Ly, and Lz describe the open passage. Extra cells outside Ly and
      ! Lz provide a periodic padding region for NGA2's FFT pressure solver.
      call param_read('Lx',Lx); call param_read('nx',nx); allocate(x(nx+1))
      call param_read('Ly',Ly); call param_read('ny',ny); allocate(y(ny+1))
      call param_read('Lz',Lz); call param_read('nz',nz); allocate(z(nz+1))
      call param_read('Wall padding cells',npad)

      if (ny.le.2*npad.or.nz.le.2*npad) error stop 'Wall padding leaves no open-channel cells'
      dy=Ly/real(ny-2*npad,WP)
      dz=Lz/real(nz-2*npad,WP)
      Ly_grid=Ly+2.0_WP*real(npad,WP)*dy
      Lz_grid=Lz+2.0_WP*real(npad,WP)*dz

      do i=1,nx+1
         x(i)=real(i-1,WP)/real(nx,WP)*Lx
      end do
      do j=1,ny+1
         y(j)=real(j-1,WP)/real(ny,WP)*Ly_grid-0.5_WP*Ly_grid
      end do
      do k=1,nz+1
         z(k)=real(k-1,WP)/real(nz,WP)*Lz_grid-0.5_WP*Lz_grid
      end do

      ! The x direction carries the imposed flow.  Periodicity in y and z is a
      ! numerical property of the padded grid, not a physical open boundary.
      grid=sgrid(coord=cartesian,no=2,x=x,y=y,z=z,&
      &          xper=.false.,yper=.true.,zper=.true.,name='srp_channel')

      create_cfg: block
         use parallel, only: group
         integer, dimension(3) :: partition
         call param_read('Partition',partition,short='p')
         cfg=ibconfig(grp=group,decomp=partition,grid=grid)
      end block create_cfg

      create_rectangular_walls: block
         use ibconfig_class, only: sharp
         do k=cfg%kmino_,cfg%kmaxo_
            do j=cfg%jmino_,cfg%jmaxo_
               do i=cfg%imino_,cfg%imaxo_
                  if (npad.eq.0) then
                     ! A zero-padding case is a fully open periodic
                     ! cross-section for uniform-flow verification.
                     cfg%Gib(i,j,k)=-min(Ly,Lz)
                  else
                     ! Gib is negative in the rectangular passage and positive
                     ! in the padding.  NGA2 converts this signed-distance-like
                     ! field into wall normals and fluid volume fractions.
                     cfg%Gib(i,j,k)=max(abs(cfg%ym(j))-0.5_WP*Ly,&
                     &                  abs(cfg%zm(k))-0.5_WP*Lz)
                  end if
               end do
            end do
         end do

         ! Optional thermo-sealed dividers between adjacent bead sticks plus
         ! edge closures from the two outer sticks to the channel walls.  The
         ! dividers span z and are rectangular in the x-y sheet cross-section.
         ! A positive Gib value denotes solid, so max() forms the union of the
         ! channel walls and every divider.  A zero default preserves all
         ! historical inputs exactly.
         separator_thickness=0.0_WP
         if (param_exists('Separator wall thickness')) &
         &  call param_read('Separator wall thickness',separator_thickness)
         if (separator_thickness.lt.0.0_WP) &
         &  error stop 'Separator wall thickness must be nonnegative'
         if (separator_thickness.gt.0.0_WP) then
            call param_read('Porous geometry',porous_geometry,default='slab')
            if (trim(porous_geometry).ne.'aligned_rods_z'.and.&
            &   trim(porous_geometry).ne.'stacked_aligned_rods_z') &
            &  error stop 'Separator walls require an aligned-rod geometry'
            call param_read('Rod count',n_rods)
            call param_read('Rod diameter',rod_diameter)
            call param_read('Rod thickness',rod_thickness,default=rod_diameter)
            call param_read('Rod center span',rod_span)
            separator_depth=rod_thickness
            if (param_exists('Separator wall depth')) &
            &  call param_read('Separator wall depth',separator_depth)
            if (n_rods.lt.2) error stop 'Separator walls require at least two rods'
            if (separator_depth.le.0.0_WP) &
            &  error stop 'Separator wall depth must be positive'
            if (trim(porous_geometry).eq.'aligned_rods_z') then
               call param_read('Rod sheet x',stack_center_x)
               n_sheets=1
               sheet_spacing=0.0_WP
            else
               call param_read('Sheet count',n_sheets)
               call param_read('Sheet spacing',sheet_spacing)
               call param_read('Stack center x',stack_center_x)
            end if
            do m=1,n_sheets
               sheet_x=stack_center_x+(real(m-1,WP)-&
               &       0.5_WP*real(n_sheets-1,WP))*sheet_spacing
               do l=0,n_rods
                  if (l.eq.0) then
                     divider_ylo=-0.5_WP*Ly
                     divider_yhi=-0.5_WP*rod_span-0.5_WP*rod_diameter
                  else if (l.eq.n_rods) then
                     divider_ylo=0.5_WP*rod_span+0.5_WP*rod_diameter
                     divider_yhi=0.5_WP*Ly
                  else
                     separator_y=-0.5_WP*rod_span+(real(l,WP)-0.5_WP)*&
                     &           rod_span/real(n_rods-1,WP)
                     divider_ylo=separator_y-0.5_WP*separator_thickness
                     divider_yhi=separator_y+0.5_WP*separator_thickness
                  end if
                  if (divider_yhi.lt.divider_ylo) &
                  &  error stop 'Outer rod extends beyond the channel wall'
                  divider_height=divider_yhi-divider_ylo
                  if (divider_height.le.0.0_WP) cycle
                  separator_y=0.5_WP*(divider_ylo+divider_yhi)
                  ! The sharp immersed-boundary reconstruction requires at
                  ! least one positive cell-center sample.  Preserve the
                  ! requested thickness when resolved; otherwise use one y
                  ! cell so a thin seal cannot disappear on a coarse grid.
                  divider_height=max(divider_height,&
                  &  1.1_WP*minval(cfg%dy(cfg%jmin_:cfg%jmax_)))
                  do k=cfg%kmino_,cfg%kmaxo_
                     do j=cfg%jmino_,cfg%jmaxo_
                        do i=cfg%imino_,cfg%imaxo_
                           divider_gib=min(0.5_WP*separator_depth-&
                           &               abs(cfg%xm(i)-sheet_x),&
                           &               0.5_WP*divider_height-&
                           &               abs(cfg%ym(j)-separator_y))
                           cfg%Gib(i,j,k)=max(cfg%Gib(i,j,k),divider_gib)
                        end do
                     end do
                  end do
               end do
            end do
         end if
         call cfg%calculate_normal()
         call cfg%calculate_vf(method=sharp,allow_zero_vf=.false.)
      end block create_rectangular_walls

   end subroutine geometry_init

end module geometry
