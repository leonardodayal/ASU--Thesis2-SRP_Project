# syntax=docker/dockerfile:1
ARG UBUNTU_VERSION=24.04

FROM ubuntu:${UBUNTU_VERSION} AS builder

ARG DEBIAN_FRONTEND=noninteractive
ARG NGA2_REPOSITORY=https://github.com/desjardi/NGA2.git
ARG NGA2_COMMIT=28a58d937af89dd506456048be1cad58f6d383a9
ARG BUILD_JOBS=4

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
      build-essential ca-certificates gfortran git libfftw3-dev libopenmpi-dev \
      make openmpi-bin perl python3 \
 && rm -rf /var/lib/apt/lists/*

RUN git init /opt/NGA2 \
 && git -C /opt/NGA2 remote add origin "${NGA2_REPOSITORY}" \
 && git -C /opt/NGA2 fetch --depth 1 origin "${NGA2_COMMIT}" \
 && git -C /opt/NGA2 checkout --detach FETCH_HEAD \
 && test "$(git -C /opt/NGA2 rev-parse HEAD)" = "${NGA2_COMMIT}" \
 && sed -i 's/ -ffast-math//g' /opt/NGA2/tools/GNUMake/comps/gnu.mak \
 && if [ "$(dpkg --print-architecture)" = "arm64" ]; then \
      sed -i 's/ -lquadmath//' /opt/NGA2/tools/GNUMake/comps/gnu.mak; \
    fi \
 && git -C /opt/NGA2 update-index --assume-unchanged tools/GNUMake/comps/gnu.mak

WORKDIR /build/srp_channel
COPY GNUmakefile ./
COPY src/ ./src/
RUN FFTW_DIR=/usr make -j"${BUILD_JOBS}" NGA_HOME=/opt/NGA2 \
 && test -x nga.dp.gnu.opt.mpi.exe

FROM ubuntu:${UBUNTU_VERSION} AS runtime

ARG DEBIAN_FRONTEND=noninteractive
ARG NGA2_COMMIT=28a58d937af89dd506456048be1cad58f6d383a9

RUN apt-get update \
 && apt-get install --no-install-recommends -y \
      libfftw3-double3 libgfortran5 openmpi-bin python3 \
 && rm -rf /var/lib/apt/lists/*

LABEL org.opencontainers.image.title="SRP NGA2 pre-calibration review package" \
      org.opencontainers.image.description="Numerical review image; geometry and porous coefficients are provisional" \
      edu.asu.srp.nga2.commit="${NGA2_COMMIT}" \
      edu.asu.srp.model-status="pre-calibration; provisional geometry and coefficients"

COPY --from=builder /build/srp_channel/nga.dp.gnu.opt.mpi.exe /opt/nga2/bin/nga2-srp-channel
COPY review/launcher.py /usr/local/bin/nga2Adsorption
COPY review/verify.py /usr/local/bin/nga2Adsorption-review
COPY review/cases/ /opt/nga2/review/cases/

RUN chmod 0755 /usr/local/bin/nga2Adsorption /usr/local/bin/nga2Adsorption-review \
 && mkdir -p /work \
 && chmod 0777 /work

WORKDIR /work
ENTRYPOINT ["nga2Adsorption"]
CMD ["--help"]
