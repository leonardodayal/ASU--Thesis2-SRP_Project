!> Rectangular SRP open-channel geometry.
module geometry
   use ibconfig_class, only: ibconfig
   use precision,      only: WP
   implicit none
   private

   type(ibconfig), public :: cfg

   public :: geometry_init

contains

   subroutine geometry_init
      use param,       only: param_read
      use sgrid_class, only: sgrid,cartesian
      implicit none
      type(sgrid) :: grid
      integer :: i,j,k,nx,ny,nz,npad
      real(WP) :: Lx,Ly,Lz,dy,dz,Ly_grid,Lz_grid
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
                  cfg%Gib(i,j,k)=max(abs(cfg%ym(j))-0.5_WP*Ly,&
                  &                  abs(cfg%zm(k))-0.5_WP*Lz)
               end do
            end do
         end do
         call cfg%calculate_normal()
         call cfg%calculate_vf(method=sharp,allow_zero_vf=.false.)
      end block create_rectangular_walls

   end subroutine geometry_init

end module geometry
