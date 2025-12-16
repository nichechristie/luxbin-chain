use crate::{mock::*, Error, Event, PhotonicColor};
use frame_support::{assert_noop, assert_ok};

#[test]
fn test_generate_temporal_key_works() {
	new_test_ext().execute_with(|| {
		// Set timestamp
		Timestamp::set_timestamp(1000000); // 1000 seconds

		let phrase = b"SECURE PAYMENT".to_vec();

		// Generate temporal key
		assert_ok!(TemporalCrypto::generate_temporal_key(
			RuntimeOrigin::signed(1),
			phrase.clone()
		));

		// Check storage
		let timestamp_secs = 1000; // 1000000ms / 1000 = 1000s
		assert!(TemporalCrypto::temporal_keys(timestamp_secs).is_some());

		// Check event
		System::assert_last_event(
			Event::TemporalKeyGenerated {
				timestamp: timestamp_secs,
				key_hash: TemporalCrypto::temporal_keys(timestamp_secs).unwrap(),
			}
			.into(),
		);
	});
}

#[test]
fn test_generate_temporal_key_fails_with_empty_phrase() {
	new_test_ext().execute_with(|| {
		Timestamp::set_timestamp(1000000);

		let empty_phrase = b"".to_vec();

		// Should fail with InvalidPhrase
		assert_noop!(
			TemporalCrypto::generate_temporal_key(
				RuntimeOrigin::signed(1),
				empty_phrase
			),
			Error::<Test>::InvalidPhrase
		);
	});
}

#[test]
fn test_photonic_encoding_works() {
	new_test_ext().execute_with(|| {
		let text = b"HELLO WORLD".to_vec();

		// Encode text
		assert_ok!(TemporalCrypto::encode_photonic(
			RuntimeOrigin::signed(1),
			text.clone()
		));

		// Check storage
		let photonic_data = TemporalCrypto::photonic_data(1).unwrap();
		assert_eq!(photonic_data.text, text);

		// Check color is valid HSL
		assert!(photonic_data.color.hue <= 360);
		assert!(photonic_data.color.saturation <= 100);
		assert!(photonic_data.color.lightness <= 100);

		// Check binary is generated
		assert!(!photonic_data.binary.is_empty());

		// Check event
		System::assert_last_event(
			Event::PhotonicEncoded {
				account: 1,
				color: photonic_data.color,
			}
			.into(),
		);
	});
}

#[test]
fn test_photonic_encoding_fails_with_invalid_chars() {
	new_test_ext().execute_with(|| {
		// Invalid characters (not in LUXBIN alphabet)
		let invalid_text = b"hello@world!".to_vec();

		// Should fail with PhotonicEncodingFailed
		assert_noop!(
			TemporalCrypto::encode_photonic(
				RuntimeOrigin::signed(1),
				invalid_text
			),
			Error::<Test>::PhotonicEncodingFailed
		);
	});
}

#[test]
fn test_photonic_encoding_empty_fails() {
	new_test_ext().execute_with(|| {
		let empty = b"".to_vec();

		// Should fail with InvalidPhrase
		assert_noop!(
			TemporalCrypto::encode_photonic(
				RuntimeOrigin::signed(1),
				empty
			),
			Error::<Test>::InvalidPhrase
		);
	});
}

#[test]
fn test_temporal_proof_validation_works() {
	new_test_ext().execute_with(|| {
		// Set current time
		let current_time = 1000000; // 1000 seconds
		Timestamp::set_timestamp(current_time);

		let timestamp = 1000; // Current time in seconds
		let phrase = b"SECRET PHRASE".to_vec();

		// Validate temporal proof
		assert_ok!(TemporalCrypto::validate_temporal_proof(
			RuntimeOrigin::signed(1),
			timestamp,
			phrase
		));

		// Check proof is stored
		let block_number = 1;
		assert!(TemporalCrypto::temporal_proofs(block_number).is_some());

		// Check event
		System::assert_last_event(
			Event::TemporalProofValidated {
				block_number,
				timestamp,
			}
			.into(),
		);
	});
}

#[test]
fn test_temporal_proof_validation_fails_outside_window() {
	new_test_ext().execute_with(|| {
		// Set current time
		let current_time = 1000000; // 1000 seconds
		Timestamp::set_timestamp(current_time);

		// Timestamp outside 30-second window
		let old_timestamp = 900; // 100 seconds ago
		let phrase = b"SECRET PHRASE".to_vec();

		// Should fail with InvalidTimestamp
		assert_noop!(
			TemporalCrypto::validate_temporal_proof(
				RuntimeOrigin::signed(1),
				old_timestamp,
				phrase
			),
			Error::<Test>::InvalidTimestamp
		);
	});
}

#[test]
fn test_timestamp_to_binary_conversion() {
	new_test_ext().execute_with(|| {
		// Test time conversion for 12:34:56
		let hours = 12u64;
		let minutes = 34u64;
		let seconds = 56u64;
		let timestamp = hours * 3600 + minutes * 60 + seconds;

		let binary = TemporalCrypto::timestamp_to_binary(timestamp);

		// Should have 17 bits (5 + 6 + 6)
		assert_eq!(binary.len(), 17);

		// Verify it's binary (only '0' and '1')
		for &byte in &binary {
			assert!(byte == b'0' || byte == b'1');
		}
	});
}

#[test]
fn test_luxbin_alphabet_encoding() {
	new_test_ext().execute_with(|| {
		// Test all valid characters
		let all_chars = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ".to_vec();

		let result = TemporalCrypto::luxbin_encode(&all_chars);
		assert!(result.is_ok());

		let photonic_data = result.unwrap();
		assert_eq!(photonic_data.text, all_chars);
		assert!(photonic_data.color.saturation == 100);
		assert!(photonic_data.color.lightness == 70);
	});
}

#[test]
fn test_temporal_key_deterministic() {
	new_test_ext().execute_with(|| {
		let timestamp = 1000u64;
		let phrase = b"TEST PHRASE".to_vec();

		// Generate key twice with same inputs
		let key1 = TemporalCrypto::compute_temporal_key(timestamp, &phrase).unwrap();
		let key2 = TemporalCrypto::compute_temporal_key(timestamp, &phrase).unwrap();

		// Should be identical (deterministic)
		assert_eq!(key1, key2);
	});
}

#[test]
fn test_temporal_key_different_times() {
	new_test_ext().execute_with(|| {
		let phrase = b"TEST PHRASE".to_vec();

		// Generate keys at different timestamps
		let key1 = TemporalCrypto::compute_temporal_key(1000, &phrase).unwrap();
		let key2 = TemporalCrypto::compute_temporal_key(2000, &phrase).unwrap();

		// Should be different
		assert_ne!(key1, key2);
	});
}

#[test]
fn test_temporal_key_different_phrases() {
	new_test_ext().execute_with(|| {
		let timestamp = 1000u64;

		// Generate keys with different phrases
		let key1 = TemporalCrypto::compute_temporal_key(timestamp, b"PHRASE ONE").unwrap();
		let key2 = TemporalCrypto::compute_temporal_key(timestamp, b"PHRASE TWO").unwrap();

		// Should be different
		assert_ne!(key1, key2);
	});
}

#[test]
fn test_verify_temporal_proof() {
	new_test_ext().execute_with(|| {
		let timestamp = 1000u64;
		let phrase = b"SECRET".to_vec();

		// Generate temporal key
		let key = TemporalCrypto::compute_temporal_key(timestamp, &phrase).unwrap();

		// Verify proof
		assert!(TemporalCrypto::verify_temporal_proof(timestamp, &phrase, key));

		// Verify with wrong phrase fails
		assert!(!TemporalCrypto::verify_temporal_proof(timestamp, b"WRONG", key));

		// Verify with wrong timestamp fails
		assert!(!TemporalCrypto::verify_temporal_proof(2000, &phrase, key));
	});
}

#[test]
fn test_photonic_color_different_texts() {
	new_test_ext().execute_with(|| {
		let text1 = b"ALICE".to_vec();
		let text2 = b"BOB".to_vec();

		let photonic1 = TemporalCrypto::luxbin_encode(&text1).unwrap();
		let photonic2 = TemporalCrypto::luxbin_encode(&text2).unwrap();

		// Different texts should produce different colors (at least different hue)
		assert_ne!(photonic1.color.hue, photonic2.color.hue);
	});
}

#[test]
fn test_photonic_binary_length() {
	new_test_ext().execute_with(|| {
		let text = b"HELLO".to_vec(); // 5 characters

		let photonic = TemporalCrypto::luxbin_encode(&text).unwrap();

		// Each character encoded with 6 bits
		// 5 characters * 6 bits = 30 bits
		assert_eq!(photonic.binary.len(), 30);
	});
}
