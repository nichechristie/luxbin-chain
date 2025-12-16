use crate as pallet_ai_compute;
use frame_support::{
	parameter_types,
	traits::{ConstU16, ConstU32, ConstU64},
};
use sp_core::H256;
use sp_runtime::{
	traits::{BlakeTwo256, IdentityLookup},
	BuildStorage,
};

type Block = frame_system::mocking::MockBlock<Test>;

// Configure a mock runtime to test the pallet.
frame_support::construct_runtime!(
	pub enum Test
	{
		System: frame_system,
		TemporalCrypto: pallet_temporal_crypto,
		AICompute: pallet_ai_compute,
		Timestamp: pallet_timestamp,
		Balances: pallet_balances,
	}
);

impl frame_system::Config for Test {
	type BaseCallFilter = frame_support::traits::Everything;
	type BlockWeights = ();
	type BlockLength = ();
	type DbWeight = ();
	type RuntimeOrigin = RuntimeOrigin;
	type RuntimeCall = RuntimeCall;
	type Nonce = u64;
	type Hash = H256;
	type Hashing = BlakeTwo256;
	type AccountId = u64;
	type Lookup = IdentityLookup<Self::AccountId>;
	type Block = Block;
	type RuntimeEvent = RuntimeEvent;
	type BlockHashCount = ConstU64<250>;
	type Version = ();
	type PalletInfo = PalletInfo;
	type AccountData = pallet_balances::AccountData<u64>;
	type OnNewAccount = ();
	type OnKilledAccount = ();
	type SystemWeightInfo = ();
	type SS58Prefix = ConstU16<42>;
	type OnSetCode = ();
	type MaxConsumers = ConstU32<16>;
}

parameter_types! {
	pub const MinimumPeriod: u64 = 1000; // 1 second
}

impl pallet_timestamp::Config for Test {
	type Moment = u64;
	type OnTimestampSet = ();
	type MinimumPeriod = MinimumPeriod;
	type WeightInfo = ();
}

parameter_types! {
	pub const ExistentialDeposit: u64 = 1;
}

impl pallet_balances::Config for Test {
	type MaxLocks = ();
	type MaxReserves = ();
	type ReserveIdentifier = [u8; 8];
	type Balance = u64;
	type RuntimeEvent = RuntimeEvent;
	type DustRemoval = ();
	type ExistentialDeposit = ExistentialDeposit;
	type AccountStore = System;
	type WeightInfo = ();
	type FreezeIdentifier = ();
	type MaxFreezes = ();
	type RuntimeHoldReason = ();
	type RuntimeFreezeReason = ();
}

parameter_types! {
	pub const TemporalWindow: u64 = 30; // 30 second validity window
}

impl pallet_temporal_crypto::Config for Test {
	type RuntimeEvent = RuntimeEvent;
	type TimeProvider = Timestamp;
	type TemporalWindow = TemporalWindow;
	type Currency = Balances;
}

parameter_types! {
	pub const MaxModelsPerNode: u32 = 10;
	pub const MaxTokensPerRequest: u32 = 100000;
}

impl pallet_ai_compute::Config for Test {
	type RuntimeEvent = RuntimeEvent;
	type Currency = Balances;
	type MaxModelsPerNode = MaxModelsPerNode;
	type MaxTokensPerRequest = MaxTokensPerRequest;
}

// Build genesis storage according to the mock runtime.
pub fn new_test_ext() -> sp_io::TestExternalities {
	let mut t = frame_system::GenesisConfig::<Test>::default()
		.build_storage()
		.unwrap();

	// Give test accounts some balance
	pallet_balances::GenesisConfig::<Test> {
		balances: vec![(1, 10000), (2, 10000), (3, 10000)],
	}
	.assimilate_storage(&mut t)
	.unwrap();

	let mut ext = sp_io::TestExternalities::new(t);
	ext.execute_with(|| {
		// Set initial timestamp
		Timestamp::set_timestamp(1000000); // Start at timestamp 1000000ms
		System::set_block_number(1);
	});
	ext
}
