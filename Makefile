# LUXBIN Development Makefile

.PHONY: help setup build test clean doc fmt clippy audit run-dev run-testnet

# Default target
help:
	@echo "LUXBIN Development Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Install development dependencies"
	@echo ""
	@echo "Building:"
	@echo "  make build          - Build the node in debug mode"
	@echo "  make build-release  - Build the node in release mode"
	@echo "  make build-runtime  - Build only the runtime"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make test-unit      - Run unit tests only"
	@echo "  make test-integration - Run integration tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make fmt            - Format code"
	@echo "  make clippy         - Run clippy linter"
	@echo "  make audit          - Run security audit"
	@echo "  make check          - Run all checks (fmt, clippy, test)"
	@echo ""
	@echo "Running:"
	@echo "  make run-dev        - Run single node development network"
	@echo "  make run-testnet    - Run local testnet (2 nodes)"
	@echo ""
	@echo "Documentation:"
	@echo "  make doc            - Generate documentation"
	@echo "  make doc-open       - Generate and open documentation"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make update         - Update dependencies"

# Setup
setup:
	@echo "Installing development dependencies..."
	rustup install nightly
	rustup target add wasm32-unknown-unknown --toolchain stable
	sudo apt-get update
	sudo apt-get install -y clang libclang-dev llvm-dev pkg-config
	cargo install cargo-husky --version "1.5.0" || true
	@echo "Setup complete! 🎉"

# Building
build:
	cargo build --manifest-path=Cargo.toml

build-release:
	cargo build --release --manifest-path=Cargo.toml

build-runtime:
	cargo build --release -p solochain-template-runtime --manifest-path=Cargo.toml

# Testing
test:
	cargo test --manifest-path=Cargo.toml

test-unit:
	cargo test --lib --manifest-path=Cargo.toml

test-integration:
	cargo test --test integration --manifest-path=Cargo.toml

# Code Quality
fmt:
	cargo fmt --all

clippy:
	cargo clippy -- -D warnings

audit:
	cargo install cargo-audit || true
	cargo audit

check: fmt clippy test
	@echo "All checks passed! ✅"

# Running
run-dev:
	@echo "Starting development network..."
	cargo build --release --bin solochain-template-node --manifest-path=Cargo.toml
	./target/release/solochain-template-node \
		--base-path /tmp/luxbin-dev \
		--chain local \
		--alice \
		--node-key 0000000000000000000000000000000000000000000000000000000000000001 \
		--validator

run-testnet:
	@echo "Starting local testnet..."
	cargo build --release --bin solochain-template-node --manifest-path=Cargo.toml
	@echo "Starting Alice node..."
	./target/release/solochain-template-node \
		--base-path /tmp/luxbin-alice \
		--chain local \
		--alice \
		--port 30333 \
		--ws-port 9944 \
		--rpc-port 9933 \
		--node-key 0000000000000000000000000000000000000000000000000000000000000001 \
		--validator &
	@echo "Waiting 5 seconds for Alice to start..."
	sleep 5
	@echo "Starting Bob node..."
	./target/release/solochain-template-node \
		--base-path /tmp/luxbin-bob \
		--chain local \
		--bob \
		--port 30334 \
		--ws-port 9945 \
		--rpc-port 9934 \
		--node-key 0000000000000000000000000000000000000000000000000000000000000002 \
		--validator \
		--bootnodes /ip4/127.0.0.1/tcp/30333/p2p/12D3KooWEyoppNCUx8Yx66oV9fJnriXwCcXwDDUA2kj6vnc6iDE

# Documentation
doc:
	cargo doc --manifest-path=Cargo.toml --no-deps --open

doc-open:
	cargo doc --manifest-path=Cargo.toml --no-deps --open

# Maintenance
clean:
	cargo clean

update:
	cargo update

# Benchmarks
bench:
	cargo bench --manifest-path=Cargo.toml

# Docker (future)
docker-build:
	docker build -t luxbin-node .

docker-run:
	docker run -p 9944:9944 -p 9933:9933 luxbin-node

# CI/CD simulation
ci: check build audit
	@echo "CI/CD checks passed! 🚀"

# Development helpers
watch:
	cargo watch -x check

# Performance profiling
profile:
	cargo build --release --bin solochain-template-node --manifest-path=Cargo.toml
	sudo perf record -F 99 -g -- target/release/solochain-template-node --dev --tmp
	sudo perf report

# Dependency analysis
deps:
	cargo tree
	cargo outdated || true
	cargo audit || true