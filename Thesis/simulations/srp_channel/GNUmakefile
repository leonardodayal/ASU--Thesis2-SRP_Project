# NGA2 source location relative to this case directory
NGA_HOME ?= ../../../NGA2

# Compilation parameters
PRECISION = DOUBLE
USE_MPI   = TRUE
USE_FFTW  = TRUE
USE_HYPRE = FALSE
USE_LAPACK= FALSE
PROFILE   = FALSE
DEBUG     = FALSE
COMP      = gnu
EXEBASE   = nga

# Thesis-owned source code
Udirs   := src
Upack   += $(foreach dir, $(Udirs), $(wildcard $(dir)/Make.package))
Ulocs   += $(foreach dir, $(Udirs), $(wildcard $(dir)))
include $(Upack)
INCLUDE_LOCATIONS += $(Ulocs)
VPATH_LOCATIONS   += $(Ulocs)

# NGA2 build definitions and base source packages
include $(NGA_HOME)/tools/GNUMake/Make.defs

Bdirs   := core constant_density data transform solver config grid libraries
Bpack   += $(foreach dir, $(Bdirs), $(NGA_HOME)/src/$(dir)/Make.package)
include $(Bpack)

ifdef Ulocs
   $(info Taking user code from: $(Ulocs))
endif
$(info Taking base code from: $(Bdirs))

all: $(executable)
	@echo COMPILATION SUCCESSFUL

include $(NGA_HOME)/tools/GNUMake/Make.rules
