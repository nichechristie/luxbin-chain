use crate::{mock::*, AIModel, Error, Event};
use frame_support::{assert_noop, assert_ok};
use sp_core::{H256, H512};

#[test]
fn test_register_ai_node_works() {
	new_test_ext().execute_with(|| {
		let models = vec![AIModel::GPT4, AIModel::ClaudeOpus];

		// Register node
		assert_ok!(AICompute::register_ai_node(
			RuntimeOrigin::signed(1),
			models.clone()
		));

		// Check storage
		assert!(AICompute::ai_nodes(1).is_some());
		let node_info = AICompute::ai_nodes(1).unwrap();
		assert_eq!(node_info.supported_models, models);
		assert!(node_info.is_active);
		assert_eq!(node_info.total_completed, 0);

		// Check event
		System::assert_last_event(
			Event::AINodeRegistered { node: 1, models }.into(),
		);
	});
}

#[test]
fn test_register_ai_node_fails_if_already_registered() {
	new_test_ext().execute_with(|| {
		let models = vec![AIModel::GPT4];

		// Register once
		assert_ok!(AICompute::register_ai_node(
			RuntimeOrigin::signed(1),
			models.clone()
		));

		// Try to register again
		assert_noop!(
			AICompute::register_ai_node(RuntimeOrigin::signed(1), models),
			Error::<Test>::AINodeAlreadyRegistered
		);
	});
}

#[test]
fn test_unregister_ai_node_works() {
	new_test_ext().execute_with(|| {
		let models = vec![AIModel::GPT4];

		// Register node
		assert_ok!(AICompute::register_ai_node(
			RuntimeOrigin::signed(1),
			models
		));

		// Unregister
		assert_ok!(AICompute::unregister_ai_node(RuntimeOrigin::signed(1)));

		// Check storage
		assert!(AICompute::ai_nodes(1).is_none());

		// Check event
		System::assert_last_event(Event::AINodeUnregistered { node: 1 }.into());
	});
}

#[test]
fn test_submit_ai_compute_request_works() {
	new_test_ext().execute_with(|| {
		// Generate temporal key (simplified for test)
		let temporal_key = H512::from_low_u64_be(12345);
		let request_hash = H256::from_low_u64_be(67890);
		let payment = 1000u64;

		// Submit request
		assert_ok!(AICompute::submit_ai_compute_request(
			RuntimeOrigin::signed(1),
			temporal_key,
			request_hash,
			AIModel::GPT4,
			10000, // max_tokens
			payment,
		));

		// Check request was created
		assert!(AICompute::ai_compute_requests(0).is_some());
		let request = AICompute::ai_compute_requests(0).unwrap();
		assert_eq!(request.requester, 1);
		assert_eq!(request.temporal_key, temporal_key);
		assert_eq!(request.request_hash, request_hash);
		assert_eq!(request.model, AIModel::GPT4);
		assert_eq!(request.payment, payment);

		// Check balance was reserved
		assert_eq!(Balances::free_balance(1), 10000 - payment);

		// Check request is in pending queue
		assert_eq!(AICompute::pending_requests(), vec![0]);

		// Check event
		System::assert_last_event(
			Event::AIComputeRequestSubmitted {
				request_id: 0,
				requester: 1,
				model: AIModel::GPT4,
				payment,
			}
			.into(),
		);
	});
}

#[test]
fn test_submit_ai_compute_request_fails_insufficient_balance() {
	new_test_ext().execute_with(|| {
		let temporal_key = H512::from_low_u64_be(12345);
		let request_hash = H256::from_low_u64_be(67890);

		// Try to submit with payment > balance
		assert_noop!(
			AICompute::submit_ai_compute_request(
				RuntimeOrigin::signed(1),
				temporal_key,
				request_hash,
				AIModel::GPT4,
				10000,
				20000, // More than balance
			),
			Error::<Test>::InsufficientBalance
		);
	});
}

#[test]
fn test_assign_ai_compute_request_works() {
	new_test_ext().execute_with(|| {
		// Register AI node
		assert_ok!(AICompute::register_ai_node(
			RuntimeOrigin::signed(2),
			vec![AIModel::GPT4]
		));

		// Submit request
		let temporal_key = H512::from_low_u64_be(12345);
		let request_hash = H256::from_low_u64_be(67890);
		assert_ok!(AICompute::submit_ai_compute_request(
			RuntimeOrigin::signed(1),
			temporal_key,
			request_hash,
			AIModel::GPT4,
			10000,
			1000,
		));

		// Assign request
		assert_ok!(AICompute::assign_ai_compute_request(
			RuntimeOrigin::signed(2),
			0
		));

		// Check request is assigned
		let request = AICompute::ai_compute_requests(0).unwrap();
		assert_eq!(request.assigned_node, Some(2));

		// Check removed from pending queue
		assert_eq!(AICompute::pending_requests(), Vec::<u64>::new());

		// Check event
		System::assert_last_event(
			Event::AIComputeRequestAssigned {
				request_id: 0,
				node: 2,
			}
			.into(),
		);
	});
}

#[test]
fn test_assign_fails_if_node_not_registered() {
	new_test_ext().execute_with(|| {
		// Submit request
		let temporal_key = H512::from_low_u64_be(12345);
		let request_hash = H256::from_low_u64_be(67890);
		assert_ok!(AICompute::submit_ai_compute_request(
			RuntimeOrigin::signed(1),
			temporal_key,
			request_hash,
			AIModel::GPT4,
			10000,
			1000,
		));

		// Try to assign without being registered
		assert_noop!(
			AICompute::assign_ai_compute_request(RuntimeOrigin::signed(2), 0),
			Error::<Test>::AINodeNotRegistered
		);
	});
}

#[test]
fn test_assign_fails_if_model_not_supported() {
	new_test_ext().execute_with(|| {
		// Register node with only GPT4
		assert_ok!(AICompute::register_ai_node(
			RuntimeOrigin::signed(2),
			vec![AIModel::GPT4]
		));

		// Submit request for ClaudeOpus
		let temporal_key = H512::from_low_u64_be(12345);
		let request_hash = H256::from_low_u64_be(67890);
		assert_ok!(AICompute::submit_ai_compute_request(
			RuntimeOrigin::signed(1),
			temporal_key,
			request_hash,
			AIModel::ClaudeOpus, // Different model
			10000,
			1000,
		));

		// Try to assign - should fail
		assert_noop!(
			AICompute::assign_ai_compute_request(RuntimeOrigin::signed(2), 0),
			Error::<Test>::ModelNotSupported
		);
	});
}

#[test]
fn test_cancel_ai_compute_request_works() {
	new_test_ext().execute_with(|| {
		// Submit request
		let temporal_key = H512::from_low_u64_be(12345);
		let request_hash = H256::from_low_u64_be(67890);
		let payment = 1000u64;
		assert_ok!(AICompute::submit_ai_compute_request(
			RuntimeOrigin::signed(1),
			temporal_key,
			request_hash,
			AIModel::GPT4,
			10000,
			payment,
		));

		// Check balance reserved
		assert_eq!(Balances::free_balance(1), 10000 - payment);

		// Cancel request
		assert_ok!(AICompute::cancel_ai_compute_request(
			RuntimeOrigin::signed(1),
			0
		));

		// Check request removed
		assert!(AICompute::ai_compute_requests(0).is_none());

		// Check balance unreserved
		assert_eq!(Balances::free_balance(1), 10000);

		// Check removed from pending queue
		assert_eq!(AICompute::pending_requests(), Vec::<u64>::new());

		// Check event
		System::assert_last_event(
			Event::AIComputeCancelled {
				request_id: 0,
				requester: 1,
			}
			.into(),
		);
	});
}

#[test]
fn test_cancel_fails_if_not_requester() {
	new_test_ext().execute_with(|| {
		// Submit request from user 1
		let temporal_key = H512::from_low_u64_be(12345);
		let request_hash = H256::from_low_u64_be(67890);
		assert_ok!(AICompute::submit_ai_compute_request(
			RuntimeOrigin::signed(1),
			temporal_key,
			request_hash,
			AIModel::GPT4,
			10000,
			1000,
		));

		// Try to cancel from user 2
		assert_noop!(
			AICompute::cancel_ai_compute_request(RuntimeOrigin::signed(2), 0),
			Error::<Test>::NotAuthorizedToCancel
		);
	});
}

#[test]
fn test_update_supported_models_works() {
	new_test_ext().execute_with(|| {
		// Register node
		assert_ok!(AICompute::register_ai_node(
			RuntimeOrigin::signed(2),
			vec![AIModel::GPT4]
		));

		// Update models
		let new_models = vec![AIModel::GPT4, AIModel::ClaudeOpus, AIModel::GeminiPro];
		assert_ok!(AICompute::update_supported_models(
			RuntimeOrigin::signed(2),
			new_models.clone()
		));

		// Check updated
		let node_info = AICompute::ai_nodes(2).unwrap();
		assert_eq!(node_info.supported_models, new_models);

		// Check event
		System::assert_last_event(
			Event::AINodeUpdated {
				node: 2,
				models: new_models,
			}
			.into(),
		);
	});
}
