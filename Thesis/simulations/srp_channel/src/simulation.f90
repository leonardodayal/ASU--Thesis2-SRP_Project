!> Constant-density flow through the empty rectangular SRP channel.
module simulation
   use precision,         only: WP
   use geometry,          only: cfg
   use fft2d_class,       only: fft2d
   use ddadi_class,       only: ddadi
   use incomp_class,      only: incomp
   use timetracker_class, only: timetracker
   use ensight_class,     only: ensight
   use event_class,       only: event
   use monitor_class,     only: monitor
   implicit none
   private

   type(incomp),      public :: fs
   type(timetracker), public :: time
   type(fft2d),       public :: ps
   type(ddadi),       public :: vs

   type(ensight) :: ens_out
   type(event)   :: ens_evt
   type(monitor) :: simfile,cflfile,flowfile,splitfile

   real(WP), dimension(:,:,:), allocatable :: resU,resV,resW
   real(WP), dimension(:,:,:), allocatable :: Ui,Vi,Wi
   real(WP), dimension(:,:,:), allocatable :: chi_p,speed_mag
   real(WP) :: darcy_coeff,forchheimer_coeff,x_pressure_up,x_pressure_down
   integer :: n_flow_bands
   real(WP) :: x_flow_split,y_flow_min,y_flow_max
   real(WP), dimension(:), allocatable, target :: band_mfr,band_fraction
   real(WP), target :: mfr_in,mfr_out,mfr_error,p_in,p_out,delta_p
   real(WP), target :: p_upstream,p_downstream,porous_delta_p
   real(WP), target :: split_mfr_sum,split_fraction_sum,flow_maldistribution

   public :: simulation_init,simulation_run,simulation_final

contains

   function left_of_domain(pg,i,j,k) result(isIn)
      use pgrid_class, only: pgrid
      class(pgrid), intent(in) :: pg
      integer, intent(in) :: i,j,k
      logical :: isIn
      isIn=(i.eq.pg%imin)
   end function left_of_domain

   function right_of_domain(pg,i,j,k) result(isIn)
      use pgrid_class, only: pgrid
      class(pgrid), intent(in) :: pg
      integer, intent(in) :: i,j,k
      logical :: isIn
      isIn=(i.eq.pg%imax+1)
   end function right_of_domain

   subroutine update_diagnostics
      use mpi_f08,  only: MPI_ALLREDUCE,MPI_SUM
      use parallel, only: MPI_REAL_WP
      integer :: i,j,k,ierr
      real(WP) :: my_pin,my_pout,my_ain,my_aout,ain,aout

      call fs%get_mfr()
      ! Boundary conditions are stored in reverse insertion order: outflow first.
      mfr_out= fs%mfr(1)
      mfr_in =-fs%mfr(2)
      mfr_error=abs(mfr_in-mfr_out)/max(abs(mfr_in),tiny(1.0_WP))

      my_pin=0.0_WP; my_pout=0.0_WP
      my_ain=0.0_WP; my_aout=0.0_WP
      if (cfg%iproc.eq.1) then
         i=cfg%imin
         do k=cfg%kmin_,cfg%kmax_
            do j=cfg%jmin_,cfg%jmax_
               my_pin=my_pin+fs%P(i,j,k)*cfg%VF(i,j,k)*cfg%dy(j)*cfg%dz(k)
               my_ain=my_ain+cfg%VF(i,j,k)*cfg%dy(j)*cfg%dz(k)
            end do
         end do
      end if
      if (cfg%iproc.eq.cfg%npx) then
         i=cfg%imax
         do k=cfg%kmin_,cfg%kmax_
            do j=cfg%jmin_,cfg%jmax_
               my_pout=my_pout+fs%P(i,j,k)*cfg%VF(i,j,k)*cfg%dy(j)*cfg%dz(k)
               my_aout=my_aout+cfg%VF(i,j,k)*cfg%dy(j)*cfg%dz(k)
            end do
         end do
      end if
      call MPI_ALLREDUCE(my_pin ,p_in ,1,MPI_REAL_WP,MPI_SUM,cfg%comm,ierr)
      call MPI_ALLREDUCE(my_pout,p_out,1,MPI_REAL_WP,MPI_SUM,cfg%comm,ierr)
      call MPI_ALLREDUCE(my_ain ,ain  ,1,MPI_REAL_WP,MPI_SUM,cfg%comm,ierr)
      call MPI_ALLREDUCE(my_aout,aout ,1,MPI_REAL_WP,MPI_SUM,cfg%comm,ierr)
      p_in=p_in/max(ain,tiny(1.0_WP))
      p_out=p_out/max(aout,tiny(1.0_WP))
      delta_p=p_in-p_out
      call sample_pressure_plane(x_pressure_up,p_upstream)
      call sample_pressure_plane(x_pressure_down,p_downstream)
      porous_delta_p=p_upstream-p_downstream
      call sample_flow_bands()
   end subroutine update_diagnostics

   subroutine initialize_flow_split
      use mpi_f08,  only: MPI_ALLREDUCE,MPI_MIN,MPI_MAX,MPI_SUM,MPI_INTEGER
      use parallel, only: MPI_REAL_WP
      integer :: i,j,k,ierr,my_plane_count,plane_count
      real(WP) :: my_ymin,my_ymax

      my_plane_count=0
      do i=cfg%imin_,cfg%imax_
         if (x_flow_split.ge.cfg%x(i).and.x_flow_split.lt.cfg%x(i+1)) &
         &  my_plane_count=my_plane_count+1
      end do
      call MPI_ALLREDUCE(my_plane_count,plane_count,1,MPI_INTEGER,MPI_SUM,cfg%comm,ierr)
      if (plane_count.eq.0) error stop 'Flow split plane lies outside the domain'

      my_ymin=huge(1.0_WP); my_ymax=-huge(1.0_WP)
      do k=cfg%kmin_,cfg%kmax_
         do j=cfg%jmin_,cfg%jmax_
            do i=cfg%imin_,cfg%imax_
               if (cfg%VF(i,j,k).gt.0.5_WP) then
                  my_ymin=min(my_ymin,cfg%y(j))
                  my_ymax=max(my_ymax,cfg%y(j+1))
               end if
            end do
         end do
      end do
      call MPI_ALLREDUCE(my_ymin,y_flow_min,1,MPI_REAL_WP,MPI_MIN,cfg%comm,ierr)
      call MPI_ALLREDUCE(my_ymax,y_flow_max,1,MPI_REAL_WP,MPI_MAX,cfg%comm,ierr)
      if (y_flow_max.le.y_flow_min) error stop 'Flow split found no open passage'
   end subroutine initialize_flow_split

   subroutine sample_flow_bands
      use mpi_f08,  only: MPI_ALLREDUCE,MPI_SUM
      use parallel, only: MPI_REAL_WP
      integer :: i,j,k,l,ierr
      real(WP) :: mean_mfr
      real(WP), dimension(n_flow_bands) :: my_band_mfr

      my_band_mfr=0.0_WP
      do i=cfg%imin_,cfg%imax_
         if (x_flow_split.ge.cfg%x(i).and.x_flow_split.lt.cfg%x(i+1)) then
            do k=cfg%kmin_,cfg%kmax_
               do j=cfg%jmin_,cfg%jmax_
                  l=1+int(real(n_flow_bands,WP)*(cfg%ym(j)-y_flow_min)/&
                  &  (y_flow_max-y_flow_min))
                  l=max(1,min(n_flow_bands,l))
                  my_band_mfr(l)=my_band_mfr(l)+fs%rho*fs%U(i,j,k)*&
                  &  cfg%dy(j)*cfg%dz(k)
               end do
            end do
         end if
      end do
      call MPI_ALLREDUCE(my_band_mfr,band_mfr,n_flow_bands,&
      &                  MPI_REAL_WP,MPI_SUM,cfg%comm,ierr)
      split_mfr_sum=sum(band_mfr)
      if (abs(split_mfr_sum).gt.tiny(1.0_WP)) then
         band_fraction=band_mfr/split_mfr_sum
      else
         band_fraction=0.0_WP
      end if
      split_fraction_sum=sum(band_fraction)
      mean_mfr=split_mfr_sum/real(n_flow_bands,WP)
      if (abs(mean_mfr).gt.tiny(1.0_WP)) then
         flow_maldistribution=sqrt(sum((band_mfr-mean_mfr)**2)/&
         &  real(n_flow_bands,WP))/abs(mean_mfr)
      else
         flow_maldistribution=0.0_WP
      end if
   end subroutine sample_flow_bands

   subroutine sample_pressure_plane(x_target,p_avg)
      use mpi_f08,  only: MPI_ALLREDUCE,MPI_SUM
      use parallel, only: MPI_REAL_WP
      real(WP), intent(in) :: x_target
      real(WP), intent(out) :: p_avg
      integer :: i,j,k,ierr
      real(WP) :: my_p,my_a,area

      my_p=0.0_WP; my_a=0.0_WP
      do i=cfg%imin_,cfg%imax_
         if (x_target.ge.cfg%x(i).and.x_target.lt.cfg%x(i+1)) then
            do k=cfg%kmin_,cfg%kmax_
               do j=cfg%jmin_,cfg%jmax_
                  my_p=my_p+fs%P(i,j,k)*cfg%VF(i,j,k)*cfg%dy(j)*cfg%dz(k)
                  my_a=my_a+cfg%VF(i,j,k)*cfg%dy(j)*cfg%dz(k)
               end do
            end do
         end if
      end do
      call MPI_ALLREDUCE(my_p,p_avg,1,MPI_REAL_WP,MPI_SUM,cfg%comm,ierr)
      call MPI_ALLREDUCE(my_a,area ,1,MPI_REAL_WP,MPI_SUM,cfg%comm,ierr)
      if (area.le.0.0_WP) error stop 'Pressure sample plane is outside the fluid domain'
      p_avg=p_avg/area
   end subroutine sample_pressure_plane

   subroutine simulation_init
      use param, only: param_exists,param_read
      implicit none

      allocate(resU(cfg%imino_:cfg%imaxo_,cfg%jmino_:cfg%jmaxo_,cfg%kmino_:cfg%kmaxo_))
      allocate(resV(cfg%imino_:cfg%imaxo_,cfg%jmino_:cfg%jmaxo_,cfg%kmino_:cfg%kmaxo_))
      allocate(resW(cfg%imino_:cfg%imaxo_,cfg%jmino_:cfg%jmaxo_,cfg%kmino_:cfg%kmaxo_))
      allocate(Ui  (cfg%imino_:cfg%imaxo_,cfg%jmino_:cfg%jmaxo_,cfg%kmino_:cfg%kmaxo_))
      allocate(Vi  (cfg%imino_:cfg%imaxo_,cfg%jmino_:cfg%jmaxo_,cfg%kmino_:cfg%kmaxo_))
      allocate(Wi  (cfg%imino_:cfg%imaxo_,cfg%jmino_:cfg%jmaxo_,cfg%kmino_:cfg%kmaxo_))
      allocate(chi_p(cfg%imino_:cfg%imaxo_,cfg%jmino_:cfg%jmaxo_,cfg%kmino_:cfg%kmaxo_))
      allocate(speed_mag(cfg%imino_:cfg%imaxo_,cfg%jmino_:cfg%jmaxo_,cfg%kmino_:cfg%kmaxo_))
      time=timetracker(amRoot=cfg%amRoot)
      call param_read('Max timestep size',time%dtmax)
      call param_read('Max cfl number',time%cflmax)
      call param_read('Max time',time%tmax)
      time%dt=time%dtmax
      time%itmax=2

      create_flow_solver: block
         use incomp_class, only: bcond,dirichlet,clipped_neumann
         type(bcond), pointer :: inflow
         integer :: i,j,k,l,m,n,n_rods,n_sheets
         real(WP) :: visc,Uin,alpha,x_start,x_end
         real(WP) :: rod_diameter,rod_span,rod_y,sheet_x
         real(WP) :: sheet_spacing,stack_center_x
         character(len=32) :: porous_geometry

         fs=incomp(cfg=cfg,name='SRP open channel')
         call param_read('Density',fs%rho)
         call param_read('Dynamic viscosity',visc); fs%visc=visc
         call param_read('Porous permeability',alpha)
         call param_read('Porous geometry',porous_geometry,default='slab')
         call param_read('Porous slab start',x_start)
         call param_read('Porous slab end',x_end)
         forchheimer_coeff=0.0_WP
         if (param_exists('Forchheimer coefficient')) &
         &  call param_read('Forchheimer coefficient',forchheimer_coeff)
         call param_read('Pressure sample upstream',x_pressure_up)
         call param_read('Pressure sample downstream',x_pressure_down)
         call param_read('Flow split bands',n_flow_bands,default=1)
         call param_read('Flow split plane',x_flow_split,default=x_pressure_down)
         if (alpha.le.0.0_WP) error stop 'Porous permeability must be positive'
         if (forchheimer_coeff.lt.0.0_WP) error stop 'Forchheimer coefficient must be nonnegative'
         if (x_end.lt.x_start) error stop 'Porous slab end must not precede its start'
         if (n_flow_bands.lt.1) error stop 'Flow split bands must be positive'
         darcy_coeff=visc/alpha
         call fs%add_bcond(name='inflow', type=dirichlet,&
         &                 locator=left_of_domain,face='x',dir=-1,canCorrect=.false.)
         call fs%add_bcond(name='outflow',type=clipped_neumann,&
         &                 locator=right_of_domain,face='x',dir=+1,canCorrect=.true.)

         ps=fft2d(cfg=cfg,name='Pressure',nst=7)
         vs=ddadi(cfg=cfg,name='Velocity',nst=7)
         call fs%setup(pressure_solver=ps,implicit_solver=vs)

         call param_read('Inlet velocity',Uin)
         chi_p=0.0_WP
         select case (trim(porous_geometry))
         case ('slab')
            do k=cfg%kmino_,cfg%kmaxo_
               do j=cfg%jmino_,cfg%jmaxo_
                  do i=cfg%imino_,cfg%imaxo_
                     if (cfg%xm(i).ge.x_start.and.cfg%xm(i).lt.x_end.and.&
                     &   cfg%VF(i,j,k).gt.0.5_WP) chi_p(i,j,k)=1.0_WP
                  end do
               end do
            end do
         case ('aligned_rods_z','stacked_aligned_rods_z')
            call param_read('Rod count',n_rods)
            call param_read('Rod diameter',rod_diameter)
            call param_read('Rod center span',rod_span)
            if (trim(porous_geometry).eq.'aligned_rods_z') then
               call param_read('Rod sheet x',stack_center_x)
               n_sheets=1
               sheet_spacing=0.0_WP
            else
               call param_read('Sheet count',n_sheets)
               call param_read('Sheet spacing',sheet_spacing)
               call param_read('Stack center x',stack_center_x)
            end if
            if (n_rods.lt.1) error stop 'Rod count must be positive'
            if (n_sheets.lt.1) error stop 'Sheet count must be positive'
            if (rod_diameter.le.0.0_WP) error stop 'Rod diameter must be positive'
            if (rod_span.lt.0.0_WP) error stop 'Rod center span must be nonnegative'
            if (sheet_spacing.lt.0.0_WP) error stop 'Sheet spacing must be nonnegative'
            do m=1,n_sheets
               if (n_sheets.eq.1) then
                  sheet_x=stack_center_x
               else
                  sheet_x=stack_center_x+(real(m-1,WP)-&
                  &       0.5_WP*real(n_sheets-1,WP))*sheet_spacing
               end if
               do l=1,n_rods
                  if (n_rods.eq.1) then
                     rod_y=0.0_WP
                  else
                     rod_y=-0.5_WP*rod_span+real(l-1,WP)*rod_span/real(n_rods-1,WP)
                  end if
                  do k=cfg%kmino_,cfg%kmaxo_
                     do j=cfg%jmino_,cfg%jmaxo_
                        do i=cfg%imino_,cfg%imaxo_
                           if ((cfg%xm(i)-sheet_x)**2+(cfg%ym(j)-rod_y)**2.le.&
                           &   (0.5_WP*rod_diameter)**2.and.&
                           &   cfg%VF(i,j,k).gt.0.5_WP) chi_p(i,j,k)=1.0_WP
                        end do
                     end do
                  end do
               end do
            end do
         case default
            error stop 'Unknown porous geometry'
         end select
         call cfg%sync(chi_p)
         fs%U=0.0_WP; fs%V=0.0_WP; fs%W=0.0_WP
         do k=cfg%kmin_,cfg%kmax_
            do j=cfg%jmin_,cfg%jmax_
               do i=cfg%imin_,cfg%imax_
                  fs%U(i,j,k)=sum(fs%itpr_x(:,i,j,k)*cfg%VF(i-1:i,j,k))*Uin
               end do
            end do
         end do
         call cfg%sync(fs%U)
         call fs%get_bcond('inflow',inflow)
         do n=1,inflow%itr%no_
            i=inflow%itr%map(1,n); j=inflow%itr%map(2,n); k=inflow%itr%map(3,n)
            fs%U(i,j,k)=cfg%VF(i,j,k)*Uin
         end do
         call fs%apply_bcond(time%t,time%dt)
         call fs%correct_mfr()
         call fs%interp_vel(Ui,Vi,Wi)
         call fs%get_div()
         allocate(band_mfr(n_flow_bands),band_fraction(n_flow_bands))
         call initialize_flow_split()
      end block create_flow_solver

      ens_out=ensight(cfg=cfg,name='srp_channel')
      ens_evt=event(time=time,name='Ensight output')
      call param_read('Ensight output period',ens_evt%tper)
      call ens_out%add_vector('velocity',Ui,Vi,Wi)
      call ens_out%add_scalar('pressure',fs%P)
      call ens_out%add_scalar('wall_vf',cfg%VF)
      call ens_out%add_scalar('porous_mask',chi_p)
      if (ens_evt%occurs()) call ens_out%write_data(time%t)

      call fs%get_cfl(time%dt,time%cfl)
      call fs%get_max()
      call update_diagnostics()

      simfile=monitor(cfg%amRoot,'simulation')
      call simfile%add_column(time%n,'Timestep number')
      call simfile%add_column(time%t,'Time')
      call simfile%add_column(time%dt,'Timestep size')
      call simfile%add_column(time%cfl,'Maximum CFL')
      call simfile%add_column(fs%Umax,'Umax')
      call simfile%add_column(fs%Vmax,'Vmax')
      call simfile%add_column(fs%Wmax,'Wmax')
      call simfile%add_column(fs%Pmax,'Pmax')
      call simfile%add_column(fs%divmax,'Maximum divergence')
      call simfile%add_column(fs%psolv%it,'Pressure iteration')
      call simfile%add_column(fs%psolv%rerr,'Pressure error')
      call simfile%write()

      cflfile=monitor(cfg%amRoot,'cfl')
      call cflfile%add_column(time%n,'Timestep number')
      call cflfile%add_column(time%t,'Time')
      call cflfile%add_column(fs%CFLc_x,'Convective xCFL')
      call cflfile%add_column(fs%CFLc_y,'Convective yCFL')
      call cflfile%add_column(fs%CFLc_z,'Convective zCFL')
      call cflfile%add_column(fs%CFLv_x,'Viscous xCFL')
      call cflfile%add_column(fs%CFLv_y,'Viscous yCFL')
      call cflfile%add_column(fs%CFLv_z,'Viscous zCFL')
      call cflfile%write()

      flowfile=monitor(cfg%amRoot,'flow_balance')
      call flowfile%add_column(time%n,'Timestep number')
      call flowfile%add_column(time%t,'Time')
      call flowfile%add_column(mfr_in,'Inlet MFR')
      call flowfile%add_column(mfr_out,'Outlet MFR')
      call flowfile%add_column(mfr_error,'Relative MFR error')
      call flowfile%add_column(p_in,'Inlet pressure')
      call flowfile%add_column(p_out,'Outlet pressure')
      call flowfile%add_column(delta_p,'Pressure drop')
      call flowfile%add_column(p_upstream,'Upstream sample pressure')
      call flowfile%add_column(p_downstream,'Downstream sample pressure')
      call flowfile%add_column(porous_delta_p,'Sample pressure drop')
      call flowfile%write()

      create_split_monitor: block
         integer :: l
         character(len=32) :: label
         splitfile=monitor(cfg%amRoot,'flow_split')
         call splitfile%add_column(time%n,'Timestep number')
         call splitfile%add_column(time%t,'Time')
         do l=1,n_flow_bands
            write(label,'("Band ",i0," MFR")') l
            call splitfile%add_column(band_mfr(l),trim(label))
            write(label,'("Band ",i0," fraction")') l
            call splitfile%add_column(band_fraction(l),trim(label))
         end do
         call splitfile%add_column(split_mfr_sum,'Band MFR sum')
         call splitfile%add_column(split_fraction_sum,'Fraction sum')
         call splitfile%add_column(flow_maldistribution,'MFR coefficient of variation')
         call splitfile%write()
      end block create_split_monitor
   end subroutine simulation_init

   subroutine simulation_run
      implicit none
      do while (.not.time%done())
         call fs%get_cfl(time%dt,time%cfl)
         call time%adjust_dt()
         call time%increment()

         fs%Uold=fs%U; fs%Vold=fs%V; fs%Wold=fs%W
         do while (time%it.le.time%itmax)
            fs%U=0.5_WP*(fs%U+fs%Uold)
            fs%V=0.5_WP*(fs%V+fs%Vold)
            fs%W=0.5_WP*(fs%W+fs%Wold)

            call fs%get_dmomdt(resU,resV,resW)
            add_porous_resistance: block
               integer :: i,j,k
               real(WP) :: chi_face,drag_coeff,speed_face
               call fs%interp_vel(Ui,Vi,Wi)
               speed_mag=sqrt(Ui**2+Vi**2+Wi**2)
               call cfg%sync(speed_mag)
               do k=cfg%kmin_,cfg%kmax_
                  do j=cfg%jmin_,cfg%jmax_
                     do i=cfg%imin_,cfg%imax_
                        chi_face=sum(fs%itpr_x(:,i,j,k)*chi_p(i-1:i,j,k))
                        speed_face=sum(fs%itpr_x(:,i,j,k)*speed_mag(i-1:i,j,k))
                        drag_coeff=darcy_coeff+0.5_WP*fs%rho*forchheimer_coeff*speed_face
                        resU(i,j,k)=resU(i,j,k)-drag_coeff*chi_face*fs%U(i,j,k)
                        chi_face=sum(fs%itpr_y(:,i,j,k)*chi_p(i,j-1:j,k))
                        speed_face=sum(fs%itpr_y(:,i,j,k)*speed_mag(i,j-1:j,k))
                        drag_coeff=darcy_coeff+0.5_WP*fs%rho*forchheimer_coeff*speed_face
                        resV(i,j,k)=resV(i,j,k)-drag_coeff*chi_face*fs%V(i,j,k)
                        chi_face=sum(fs%itpr_z(:,i,j,k)*chi_p(i,j,k-1:k))
                        speed_face=sum(fs%itpr_z(:,i,j,k)*speed_mag(i,j,k-1:k))
                        drag_coeff=darcy_coeff+0.5_WP*fs%rho*forchheimer_coeff*speed_face
                        resW(i,j,k)=resW(i,j,k)-drag_coeff*chi_face*fs%W(i,j,k)
                     end do
                  end do
               end do
            end block add_porous_resistance
            resU=-2.0_WP*(fs%rho*fs%U-fs%rho*fs%Uold)+time%dt*resU
            resV=-2.0_WP*(fs%rho*fs%V-fs%rho*fs%Vold)+time%dt*resV
            resW=-2.0_WP*(fs%rho*fs%W-fs%rho*fs%Wold)+time%dt*resW
            call fs%solve_implicit(time%dt,resU,resV,resW)
            fs%U=2.0_WP*fs%U-fs%Uold+resU
            fs%V=2.0_WP*fs%V-fs%Vold+resV
            fs%W=2.0_WP*fs%W-fs%Wold+resW

            enforce_stationary_walls: block
               integer :: i,j,k
               real(WP) :: vf
               do k=cfg%kmin_,cfg%kmax_
                  do j=cfg%jmin_,cfg%jmax_
                     do i=cfg%imin_,cfg%imax_
                        if (fs%umask(i,j,k).eq.0) then
                           vf=sum(fs%itpr_x(:,i,j,k)*cfg%VF(i-1:i,j,k))
                           fs%U(i,j,k)=vf*fs%U(i,j,k)
                        end if
                        if (fs%vmask(i,j,k).eq.0) then
                           vf=sum(fs%itpr_y(:,i,j,k)*cfg%VF(i,j-1:j,k))
                           fs%V(i,j,k)=vf*fs%V(i,j,k)
                        end if
                        if (fs%wmask(i,j,k).eq.0) then
                           vf=sum(fs%itpr_z(:,i,j,k)*cfg%VF(i,j,k-1:k))
                           fs%W(i,j,k)=vf*fs%W(i,j,k)
                        end if
                     end do
                  end do
               end do
               call cfg%sync(fs%U); call cfg%sync(fs%V); call cfg%sync(fs%W)
            end block enforce_stationary_walls

            call fs%apply_bcond(time%t,time%dt)
            call fs%correct_mfr()
            call fs%get_div()
            fs%psolv%rhs=-cfg%vol*fs%div*fs%rho/time%dt
            fs%psolv%sol=0.0_WP
            call fs%psolv%solve()
            call fs%shift_p(fs%psolv%sol)
            call fs%get_pgrad(fs%psolv%sol,resU,resV,resW)
            fs%P=fs%P+fs%psolv%sol
            fs%U=fs%U-time%dt*resU/fs%rho
            fs%V=fs%V-time%dt*resV/fs%rho
            fs%W=fs%W-time%dt*resW/fs%rho
            time%it=time%it+1
         end do

         call fs%interp_vel(Ui,Vi,Wi)
         call fs%get_div()
         if (ens_evt%occurs()) call ens_out%write_data(time%t)
         call fs%get_max()
         call update_diagnostics()
         call simfile%write()
         call cflfile%write()
         call flowfile%write()
         call splitfile%write()
      end do
   end subroutine simulation_run

   subroutine simulation_final
      implicit none
      call simfile%finalize()
      call cflfile%finalize()
      call flowfile%finalize()
      call splitfile%finalize()
      deallocate(resU,resV,resW,Ui,Vi,Wi,chi_p,speed_mag,band_mfr,band_fraction)
   end subroutine simulation_final

end module simulation
