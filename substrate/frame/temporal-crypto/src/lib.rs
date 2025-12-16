#![cfg_attr(not(feature = "std"), no_std)]

//! # LUXBIN Temporal Cryptography Pallet
//!
//! Revolutionary time-based cryptographic key generation and photonic encoding.
//!
//! ## Overview
//!
//! This pallet implements:
//! - Temporal key generation (time → cryptographic keys)
//! - Photonic encoding (text → HSL light wavelengths → binary)
//! - Proof-of-Time validation for blockchain consensus
//! - **AI Compute Gating** (temporal-locked access to AI nodes)
//!
//! ## Temporal Cryptography
//!
//! Instead of proof-of-work mining, LUXBIN uses time-based consensus where
//! cryptographic keys can only be generated at specific timestamps.
//!
//! ## AI Compute Network
//!
//! LUXBIN enables decentralized AI computation with temporal cryptographic access control:
//! - Users generate temporal keys to request AI computation
//! - Blockchain verifies temporal proofs and routes requests to AI nodes
//! - AI nodes compute results and submit HMAC-signed outputs
//! - Blockchain verifies outputs and releases payments automatically

pub use pallet::*;

use frame_support::{
	pallet_prelude::*,
	traits::{Currency, Time, ReservableCurrency},
};
use frame_system::pallet_prelude::*;
use sp_core::{H256, H512, ConstU32};
// use sp_runtime::traits::Hash; // Not used currently
use sp_std::vec::Vec;
use sha3::{Digest, Sha3_512};

type BalanceOf<T> = <<T as Config>::Currency as Currency<<T as frame_system::Config>::AccountId>>::Balance;

#[cfg(test)]
mod mock;

#[cfg(test)]
mod tests;

/// LUXBIN alphabet for photonic encoding
const LUXBIN_ALPHABET: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ";

/// Photonic color representation (HSL)
#[derive(Clone, Encode, Decode, TypeInfo, MaxEncodedLen, PartialEq, Eq, Debug, DecodeWithMemTracking)]
#[scale_info(skip_type_params(T))]
pub struct PhotonicColor {
	/// Hue: 0-360 degrees
	pub hue: u16,
	/// Saturation: 0-100%
	pub saturation: u8,
	/// Lightness: 0-100%
	pub lightness: u8,
}

/// Photonic data encoding
#[derive(Clone, Encode, Decode, TypeInfo, MaxEncodedLen)]
#[scale_info(skip_type_params(T))]
pub struct PhotonicData {
	/// Original text (max 1024 bytes)
	pub text: BoundedVec<u8, ConstU32<1024>>,
	/// HSL color representation
	pub color: PhotonicColor,
	/// Binary representation (max 4096 bytes)
	pub binary: BoundedVec<u8, ConstU32<4096>>,
}

/// Temporal proof for consensus
#[derive(Clone, Encode, Decode, TypeInfo, MaxEncodedLen)]
#[scale_info(skip_type_params(T))]
pub struct TemporalProof<Moment> {
	/// Timestamp used for key generation
	pub timestamp: Moment,
	/// Generated temporal key
	pub temporal_key: H512,
	/// Phrase hash (for verification)
	pub phrase_hash: H512,
}

/// AI Compute Request Status
#[derive(Clone, Encode, Decode, TypeInfo, MaxEncodedLen, PartialEq, Eq)]
pub enum AIComputeStatus {
	/// Request submitted, waiting for assignment
	Pending,
	/// Assigned to AI node
	Assigned,
	/// AI node computing result
	Computing,
	/// Result submitted, waiting for verification
	Verifying,
	/// Computation completed and verified
	Completed,
	/// Computation failed or rejected
	Failed,
}

/// AI Compute Request
#[derive(Clone, Encode, Decode, TypeInfo, MaxEncodedLen)]
#[scale_info(skip_type_params(T))]
pub struct AIComputeRequest<AccountId, Balance, Moment> {
	/// User who submitted the request
	pub requester: AccountId,
	/// Temporal key for access control
	pub temporal_key: H512,
	/// Hash of the AI prompt/request
	pub request_hash: H256,
	/// Timestamp when request was created
	pub timestamp: Moment,
	/// Payment amount in LUXBIN tokens
	pub payment: Balance,
	/// Assigned AI node (None if not assigned)
	pub assigned_node: Option<AccountId>,
	/// Current status
	pub status: AIComputeStatus,
}

/// AI Compute Result
#[derive(Clone, Encode, Decode, TypeInfo, MaxEncodedLen)]
#[scale_info(skip_type_params(T))]
pub struct AIComputeResult<AccountId> {
	/// Hash of the AI output
	pub output_hash: H256,
	/// HMAC of output using temporal key
	pub output_hmac: H512,
	/// AI node that computed the result
	pub node: AccountId,
	/// Temporal proof that computation happened at valid time
	pub temporal_proof: H512,
}

#[frame_support::pallet]
pub mod pallet {
	use super::*;

	#[pallet::pallet]
	pub struct Pallet<T>(_);

	#[pallet::config]
	pub trait Config: frame_system::Config {
		/// The overarching event type.
		type RuntimeEvent: From<Event<Self>> + IsType<<Self as frame_system::Config>::RuntimeEvent>;

		/// Time provider for temporal key generation
		type TimeProvider: Time<Moment = u64>;

		/// Temporal key validity window (in seconds)
		#[pallet::constant]
		type TemporalWindow: Get<u64>;

		/// Currency for AI compute payments
		type Currency: Currency<Self::AccountId> + ReservableCurrency<Self::AccountId>;
	}

	/// Storage for temporal keys indexed by timestamp
	#[pallet::storage]
	#[pallet::getter(fn temporal_keys)]
	pub type TemporalKeys<T: Config> = StorageMap<
		_,
		Blake2_128Concat,
		u64, // timestamp
		H512, // temporal key
		OptionQuery,
	>;

	/// Storage for photonic encodings indexed by account
	#[pallet::storage]
	#[pallet::getter(fn photonic_data)]
	pub type PhotonicStorage<T: Config> = StorageMap<
		_,
		Blake2_128Concat,
		T::AccountId,
		PhotonicData,
		OptionQuery,
	>;

	/// Storage for temporal proofs indexed by block number
	#[pallet::storage]
	#[pallet::getter(fn temporal_proofs)]
	pub type TemporalProofs<T: Config> = StorageMap<
		_,
		Blake2_128Concat,
		BlockNumberFor<T>,
		TemporalProof<u64>,
		OptionQuery,
	>;

	/// Counter for AI compute request IDs
	#[pallet::storage]
	#[pallet::getter(fn next_request_id)]
	pub type NextRequestId<T: Config> = StorageValue<_, u64, ValueQuery>;

	/// Storage for AI compute requests indexed by request ID
	#[pallet::storage]
	#[pallet::getter(fn ai_compute_requests)]
	pub type AIComputeRequests<T: Config> = StorageMap<
		_,
		Blake2_128Concat,
		u64, // request_id
		AIComputeRequest<T::AccountId, BalanceOf<T>, u64>,
		OptionQuery,
	>;

	/// Storage for AI compute results indexed by request ID
	#[pallet::storage]
	#[pallet::getter(fn ai_compute_results)]
	pub type AIComputeResults<T: Config> = StorageMap<
		_,
		Blake2_128Concat,
		u64, // request_id
		AIComputeResult<T::AccountId>,
		OptionQuery,
	>;

	/// Storage for AI node registrations
	#[pallet::storage]
	#[pallet::getter(fn ai_nodes)]
	pub type AINodes<T: Config> = StorageMap<
		_,
		Blake2_128Concat,
		T::AccountId,
		bool, // is_active
		ValueQuery,
	>;

	#[pallet::event]
	#[pallet::generate_deposit(pub(super) fn deposit_event)]
	pub enum Event<T: Config> {
		/// Temporal key generated [timestamp, key_hash]
		TemporalKeyGenerated { timestamp: u64, key_hash: H512 },
		/// Photonic data encoded [account, color]
		PhotonicEncoded { account: T::AccountId, color: PhotonicColor },
		/// Temporal proof validated [block_number, timestamp]
		TemporalProofValidated { block_number: BlockNumberFor<T>, timestamp: u64 },
		/// Temporal proof failed [block_number, reason]
		TemporalProofFailed { block_number: BlockNumberFor<T>, reason: Vec<u8> },
		/// AI node registered
		AINodeRegistered { node: T::AccountId },
		/// AI node unregistered
		AINodeUnregistered { node: T::AccountId },
		/// AI compute request submitted
		AIComputeRequestSubmitted { request_id: u64, requester: T::AccountId, payment: BalanceOf<T> },
		/// AI compute request assigned to node
		AIComputeRequestAssigned { request_id: u64, node: T::AccountId },
		/// AI compute result submitted
		AIComputeResultSubmitted { request_id: u64, node: T::AccountId },
		/// AI compute verified and payment released
		AIComputeVerified { request_id: u64, node: T::AccountId, payment: BalanceOf<T> },
		/// AI compute failed
		AIComputeFailed { request_id: u64, reason: Vec<u8> },
	}

	#[pallet::error]
	pub enum Error<T> {
		/// Invalid timestamp (outside temporal window)
		InvalidTimestamp,
		/// Invalid phrase (empty or invalid characters)
		InvalidPhrase,
		/// Temporal key already exists for timestamp
		TemporalKeyExists,
		/// Temporal proof validation failed
		ProofValidationFailed,
		/// Photonic encoding failed
		PhotonicEncodingFailed,
		/// AI node already registered
		AINodeAlreadyRegistered,
		/// AI node not registered
		AINodeNotRegistered,
		/// AI compute request not found
		AIComputeRequestNotFound,
		/// Insufficient balance for AI compute payment
		InsufficientBalance,
		/// Invalid AI compute request
		InvalidAIComputeRequest,
		/// AI compute result verification failed
		AIComputeVerificationFailed,
		/// Not authorized (only assigned node can submit result)
		NotAuthorizedNode,
		/// Request already completed
		RequestAlreadyCompleted,
	}

	#[pallet::call]
	impl<T: Config> Pallet<T> {
		/// Generate a temporal key for the current timestamp
		///
		/// # Parameters
		/// - `phrase`: Secret phrase to combine with timestamp
		///
		/// # Weight
		/// O(1) - Fixed cryptographic operations
		#[pallet::call_index(0)]
		#[pallet::weight(10_000)]
		pub fn generate_temporal_key(
			origin: OriginFor<T>,
			phrase: Vec<u8>,
		) -> DispatchResult {
			let _who = ensure_signed(origin)?;

			// Get current timestamp
			let timestamp = T::TimeProvider::now();
			let timestamp_secs = timestamp / 1000; // Convert to seconds

			// Validate phrase
			ensure!(!phrase.is_empty(), Error::<T>::InvalidPhrase);

			// Generate temporal key
			let temporal_key = Self::compute_temporal_key(timestamp_secs, &phrase)?;

			// Store temporal key
			TemporalKeys::<T>::insert(timestamp_secs, temporal_key);

			// Emit event
			Self::deposit_event(Event::TemporalKeyGenerated {
				timestamp: timestamp_secs,
				key_hash: temporal_key,
			});

			Ok(())
		}

		/// Encode text using photonic encoding (LUXBIN)
		///
		/// # Parameters
		/// - `text`: Text to encode (must use LUXBIN alphabet)
		///
		/// # Weight
		/// O(n) where n is text length
		#[pallet::call_index(1)]
		#[pallet::weight(10_000)]
		pub fn encode_photonic(
			origin: OriginFor<T>,
			text: Vec<u8>,
		) -> DispatchResult {
			let who = ensure_signed(origin)?;

			// Validate and encode
			let photonic_data = Self::luxbin_encode(&text)?;

			// Store photonic data
			PhotonicStorage::<T>::insert(&who, photonic_data.clone());

			// Emit event
			Self::deposit_event(Event::PhotonicEncoded {
				account: who,
				color: photonic_data.color,
			});

			Ok(())
		}

		/// Validate temporal proof for block
		///
		/// # Parameters
		/// - `timestamp`: Claimed timestamp
		/// - `phrase`: Secret phrase used for key generation
		///
		/// # Weight
		/// O(1) - Fixed cryptographic operations
		#[pallet::call_index(2)]
		#[pallet::weight(10_000)]
		pub fn validate_temporal_proof(
			origin: OriginFor<T>,
			timestamp: u64,
			phrase: Vec<u8>,
		) -> DispatchResult {
			ensure_signed(origin)?;

			let current_block = frame_system::Pallet::<T>::block_number();
			let current_time = T::TimeProvider::now() / 1000;

			// Validate timestamp is within temporal window
			let window = T::TemporalWindow::get();
			ensure!(
				timestamp >= current_time.saturating_sub(window) &&
				timestamp <= current_time.saturating_add(window),
				Error::<T>::InvalidTimestamp
			);

			// Compute temporal key
			let temporal_key = Self::compute_temporal_key(timestamp, &phrase)?;

			// Create proof
			let phrase_hash = Self::hash_phrase(&phrase);
			let proof = TemporalProof {
				timestamp,
				temporal_key,
				phrase_hash,
			};

			// Store proof
			TemporalProofs::<T>::insert(current_block, proof);

			// Emit event
			Self::deposit_event(Event::TemporalProofValidated {
				block_number: current_block,
				timestamp,
			});

			Ok(())
		}

		/// Register as an AI compute node
		///
		/// # Weight
		/// O(1)
		#[pallet::call_index(3)]
		#[pallet::weight(10_000)]
		pub fn register_ai_node(origin: OriginFor<T>) -> DispatchResult {
			let who = ensure_signed(origin)?;

			// Check not already registered
			ensure!(!AINodes::<T>::get(&who), Error::<T>::AINodeAlreadyRegistered);

			// Register node
			AINodes::<T>::insert(&who, true);

			// Emit event
			Self::deposit_event(Event::AINodeRegistered { node: who });

			Ok(())
		}

		/// Unregister as an AI compute node
		///
		/// # Weight
		/// O(1)
		#[pallet::call_index(4)]
		#[pallet::weight(10_000)]
		pub fn unregister_ai_node(origin: OriginFor<T>) -> DispatchResult {
			let who = ensure_signed(origin)?;

			// Check is registered
			ensure!(AINodes::<T>::get(&who), Error::<T>::AINodeNotRegistered);

			// Unregister node
			AINodes::<T>::remove(&who);

			// Emit event
			Self::deposit_event(Event::AINodeUnregistered { node: who });

			Ok(())
		}

		/// Submit an AI compute request with temporal key
		///
		/// # Parameters
		/// - `temporal_key`: Temporal cryptographic key for access control
		/// - `request_hash`: Hash of the AI prompt/request data
		/// - `payment`: Amount to pay for computation
		///
		/// # Weight
		/// O(1)
		#[pallet::call_index(5)]
		#[pallet::weight(10_000)]
		pub fn submit_ai_compute_request(
			origin: OriginFor<T>,
			temporal_key: H512,
			request_hash: H256,
			payment: BalanceOf<T>,
		) -> DispatchResult {
			let who = ensure_signed(origin)?;

			// Verify user has sufficient balance
			ensure!(
				T::Currency::can_reserve(&who, payment),
				Error::<T>::InsufficientBalance
			);

			// Reserve payment
			T::Currency::reserve(&who, payment)?;

			// Get current timestamp
			let timestamp = T::TimeProvider::now() / 1000;

			// Create request ID
			let request_id = NextRequestId::<T>::get();
			NextRequestId::<T>::put(request_id + 1);

			// Create request
			let request = AIComputeRequest {
				requester: who.clone(),
				temporal_key,
				request_hash,
				timestamp,
				payment,
				assigned_node: None,
				status: AIComputeStatus::Pending,
			};

			// Store request
			AIComputeRequests::<T>::insert(request_id, request);

			// Emit event
			Self::deposit_event(Event::AIComputeRequestSubmitted {
				request_id,
				requester: who,
				payment,
			});

			Ok(())
		}

		/// Assign AI compute request to a node (can be called by node)
		///
		/// # Parameters
		/// - `request_id`: ID of the request to assign
		///
		/// # Weight
		/// O(1)
		#[pallet::call_index(6)]
		#[pallet::weight(10_000)]
		pub fn assign_ai_compute_request(
			origin: OriginFor<T>,
			request_id: u64,
		) -> DispatchResult {
			let who = ensure_signed(origin)?;

			// Verify node is registered
			ensure!(AINodes::<T>::get(&who), Error::<T>::AINodeNotRegistered);

			// Get request
			let mut request = AIComputeRequests::<T>::get(request_id)
				.ok_or(Error::<T>::AIComputeRequestNotFound)?;

			// Verify request is pending
			ensure!(
				request.status == AIComputeStatus::Pending,
				Error::<T>::InvalidAIComputeRequest
			);

			// Assign to node
			request.assigned_node = Some(who.clone());
			request.status = AIComputeStatus::Assigned;

			// Update request
			AIComputeRequests::<T>::insert(request_id, request);

			// Emit event
			Self::deposit_event(Event::AIComputeRequestAssigned {
				request_id,
				node: who,
			});

			Ok(())
		}

		/// Submit AI compute result with HMAC verification
		///
		/// # Parameters
		/// - `request_id`: ID of the request
		/// - `output_hash`: Hash of the AI output
		/// - `output_hmac`: HMAC of output using temporal key
		///
		/// # Weight
		/// O(1)
		#[pallet::call_index(7)]
		#[pallet::weight(10_000)]
		pub fn submit_ai_compute_result(
			origin: OriginFor<T>,
			request_id: u64,
			output_hash: H256,
			output_hmac: H512,
		) -> DispatchResult {
			let who = ensure_signed(origin)?;

			// Get request
			let mut request = AIComputeRequests::<T>::get(request_id)
				.ok_or(Error::<T>::AIComputeRequestNotFound)?;

			// Verify caller is assigned node
			ensure!(
				request.assigned_node == Some(who.clone()),
				Error::<T>::NotAuthorizedNode
			);

			// Verify not already completed
			ensure!(
				request.status != AIComputeStatus::Completed,
				Error::<T>::RequestAlreadyCompleted
			);

			// Verify HMAC matches temporal key
			let temporal_proof = Self::verify_ai_output_hmac(
				&request.temporal_key,
				&output_hash,
				&output_hmac,
			)?;

			// Create result
			let result = AIComputeResult {
				output_hash,
				output_hmac,
				node: who.clone(),
				temporal_proof,
			};

			// Store result
			AIComputeResults::<T>::insert(request_id, result);

			// Update request status
			request.status = AIComputeStatus::Completed;
			AIComputeRequests::<T>::insert(request_id, request.clone());

			// Release payment to node
			T::Currency::unreserve(&request.requester, request.payment);
			T::Currency::transfer(
				&request.requester,
				&who,
				request.payment,
				frame_support::traits::ExistenceRequirement::KeepAlive,
			)?;

			// Emit event
			Self::deposit_event(Event::AIComputeVerified {
				request_id,
				node: who,
				payment: request.payment,
			});

			Ok(())
		}
	}
}

impl<T: Config> Pallet<T> {
	/// Core temporal key generation algorithm
	///
	/// # Process:
	/// 1. Convert timestamp to binary
	/// 2. Encode phrase using LUXBIN photonic encoding
	/// 3. Combine time binary + photonic binary
	/// 4. Hash with SHA3-512
	///
	/// # Returns
	/// 512-bit temporal cryptographic key
	fn compute_temporal_key(timestamp: u64, phrase: &[u8]) -> Result<H512, Error<T>> {
		// 1. Time to binary
		let time_binary = Self::timestamp_to_binary(timestamp);

		// 2. Phrase to LUXBIN photonic
		let photonic_data = Self::luxbin_encode(phrase)?;

		// 3. Combine binaries
		let mut combined = time_binary;
		combined.extend_from_slice(&photonic_data.binary);

		// 4. Hash with SHA3-512
		let mut hasher = Sha3_512::new();
		hasher.update(&combined);
		let result = hasher.finalize();

		Ok(H512::from_slice(&result[..]))
	}

	/// Convert timestamp to binary representation
	///
	/// Format: HH:MM:SS → binary concatenation
	fn timestamp_to_binary(timestamp: u64) -> Vec<u8> {
		let hours = (timestamp / 3600) % 24;
		let minutes = (timestamp / 60) % 60;
		let seconds = timestamp % 60;

		let mut binary = Vec::new();
		binary.extend_from_slice(&Self::u64_to_binary(hours, 5)); // 0-23 needs 5 bits
		binary.extend_from_slice(&Self::u64_to_binary(minutes, 6)); // 0-59 needs 6 bits
		binary.extend_from_slice(&Self::u64_to_binary(seconds, 6)); // 0-59 needs 6 bits

		binary
	}

	/// Convert u64 to binary with specified bit length
	fn u64_to_binary(value: u64, bits: usize) -> Vec<u8> {
		let mut binary = Vec::new();
		for i in (0..bits).rev() {
			binary.push(if (value >> i) & 1 == 1 { b'1' } else { b'0' });
		}
		binary
	}

	/// LUXBIN photonic encoding
	///
	/// Maps characters to HSL color space:
	/// - Each character → unique hue angle (0-360°)
	/// - Saturation: 100% (fully saturated)
	/// - Lightness: 70% (optimal visibility)
	fn luxbin_encode(text: &[u8]) -> Result<PhotonicData, Error<T>> {
		ensure!(!text.is_empty(), Error::<T>::InvalidPhrase);

		let text_str = sp_std::str::from_utf8(text)
			.map_err(|_| Error::<T>::PhotonicEncodingFailed)?;

		// Validate characters are in LUXBIN alphabet
		for c in text_str.chars() {
			ensure!(
				LUXBIN_ALPHABET.contains(c),
				Error::<T>::PhotonicEncodingFailed
			);
		}

		// Calculate average position for color encoding
		let mut total_pos = 0u64;
		for c in text_str.chars() {
			if let Some(pos) = LUXBIN_ALPHABET.find(c) {
				total_pos += pos as u64;
			}
		}

		let avg_pos = total_pos / (text_str.len() as u64);
		let alphabet_len = LUXBIN_ALPHABET.len() as u64;

		// Map to HSL
		let hue = ((avg_pos * 360) / alphabet_len) as u16;
		let saturation = 100u8;
		let lightness = 70u8;

		let color = PhotonicColor { hue, saturation, lightness };

		// Generate binary representation
		let mut binary_vec = Vec::new();
		for c in text_str.chars() {
			if let Some(pos) = LUXBIN_ALPHABET.find(c) {
				// 6 bits per character (37 chars fits in 6 bits: 2^6 = 64)
				binary_vec.extend_from_slice(&Self::u64_to_binary(pos as u64, 6));
			}
		}

		let text_bounded = BoundedVec::try_from(text.to_vec())
			.map_err(|_| Error::<T>::PhotonicEncodingFailed)?;
		let binary_bounded = BoundedVec::try_from(binary_vec)
			.map_err(|_| Error::<T>::PhotonicEncodingFailed)?;

		Ok(PhotonicData {
			text: text_bounded,
			color,
			binary: binary_bounded,
		})
	}

	/// Hash phrase for verification
	fn hash_phrase(phrase: &[u8]) -> H512 {
		let mut hasher = Sha3_512::new();
		hasher.update(phrase);
		let result = hasher.finalize();
		H512::from_slice(&result[..])
	}

	/// Verify temporal proof is valid
	pub fn verify_temporal_proof(
		timestamp: u64,
		phrase: &[u8],
		expected_key: H512,
	) -> bool {
		if let Ok(computed_key) = Self::compute_temporal_key(timestamp, phrase) {
			computed_key == expected_key
		} else {
			false
		}
	}

	/// Verify AI output HMAC using temporal key
	///
	/// # Process:
	/// 1. Combine output_hash + temporal_key
	/// 2. Hash with SHA3-512
	/// 3. Compare with provided HMAC
	///
	/// # Returns
	/// Temporal proof hash if valid, error otherwise
	fn verify_ai_output_hmac(
		temporal_key: &H512,
		output_hash: &H256,
		output_hmac: &H512,
	) -> Result<H512, Error<T>> {
		// Combine output hash and temporal key
		let mut combined = Vec::new();
		combined.extend_from_slice(output_hash.as_bytes());
		combined.extend_from_slice(temporal_key.as_bytes());

		// Compute HMAC
		let mut hasher = Sha3_512::new();
		hasher.update(&combined);
		let result = hasher.finalize();
		let computed_hmac = H512::from_slice(&result[..]);

		// Verify HMAC matches
		ensure!(
			&computed_hmac == output_hmac,
			Error::<T>::AIComputeVerificationFailed
		);

		// Return temporal proof (hash of the HMAC for verification)
		let mut proof_hasher = Sha3_512::new();
		proof_hasher.update(output_hmac.as_bytes());
		let proof_result = proof_hasher.finalize();
		Ok(H512::from_slice(&proof_result[..]))
	}
}
