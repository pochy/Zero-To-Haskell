FROM haskell:9.10

ENV PATH="/opt/ghc/9.10.3/bin:${PATH}"

WORKDIR /workspace

RUN cabal update

COPY cabal.project haskell-complete-tutorial.cabal ./
COPY src ./src
COPY test ./test

RUN cabal build all --only-dependencies || true

CMD ["/bin/bash"]
