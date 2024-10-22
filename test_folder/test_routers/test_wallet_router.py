import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from starlette import status
from business_layer.wallet import Wallet
from utils.Exceptions import (SelfTransferException, WalletEmptyException,
                              LowBalanceException, DatabaseException,
                              InvalidAmountException)
from fastapi import HTTPException
from main import app  # Assuming this is the main FastAPI app
from datetime import timedelta
from tokens.tokens import create_access_token  # Import token creation

client = TestClient(app)


class TestSendAmountEndpoint(unittest.TestCase):

    def setUp(self):
        self.username = "ad123"
        self.token = self.create_test_token(self.username)

    def create_test_token(self, username):
        return create_access_token(username, timedelta(minutes=20))

    @patch('tokens.tokens.get_current_user')
    @patch('routers.wallet_router.create_wallet_from_username')
    @patch('business_layer.authentication.Authentication.check_if_username_exists')
    @patch('routers.wallet_router.transaction_dictionary')
    def test_successful_send_amount(self, mock_transaction_dict, mock_check_user_exists,
                                    mock_create_wallet, mock_get_current_user):
        # Arrange
        mock_get_current_user.return_value = self.username
        mock_check_user_exists.return_value = True
        mock_create_wallet.return_value.send_amount.return_value = MagicMock()
        mock_create_wallet.return_value.receive_amount.return_value = None
        mock_transaction_dict.return_value = {"transaction": "details"}

        # Act
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post("/wallet/send", params={"receiver": "receiver_user", "amount": 100}, headers=headers)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"transaction": "details"})

    @patch('tokens.tokens.get_current_user')
    @patch('routers.wallet_router.create_wallet_from_username')
    @patch('business_layer.authentication.Authentication.check_if_username_exists')
    def test_send_amount_receiver_not_found(self, mock_check_user_exists,
                                            mock_create_wallet, mock_get_current_user):
        # Arrange
        mock_get_current_user.return_value = self.username
        mock_check_user_exists.return_value = False
        mock_create_wallet.return_value.send_amount.return_value = MagicMock()
        mock_create_wallet.return_value.receive_amount.return_value = None

        # Act
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post("/wallet/send", params={"receiver": "receiver_user", "amount": 100}, headers=headers)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'detail': 'Receiver does not exist'})

    @patch('tokens.tokens.get_current_user')
    @patch('routers.wallet_router.create_wallet_from_username')
    @patch('business_layer.authentication.Authentication.check_if_username_exists')
    def test_send_amount_failure_self_transfer(self, mock_check_user_exists,
                                               mock_create_wallet, mock_get_current_user):
        # Arrange
        mock_get_current_user.return_value = self.username
        mock_check_user_exists.return_value = True
        mock_create_wallet.return_value.send_amount.side_effect = SelfTransferException()

        # Act
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post("/wallet/send", params={"receiver": "receiver_user", "amount": 100}, headers=headers)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Cannot transfer to the same account wallet!'})

    @patch('tokens.tokens.get_current_user')
    @patch('routers.wallet_router.create_wallet_from_username')
    @patch('business_layer.authentication.Authentication.check_if_username_exists')
    def test_send_amount_failure_wallet_empty(self, mock_check_user_exists,
                                              mock_create_wallet, mock_get_current_user):
        # Arrange
        mock_get_current_user.return_value = self.username
        mock_check_user_exists.return_value = True
        mock_create_wallet.return_value.send_amount.side_effect = WalletEmptyException()

        # Act
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post("/wallet/send", params={"receiver": "receiver_user", "amount": 100}, headers=headers)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'User wallet is empty!'})

    @patch('tokens.tokens.get_current_user')
    @patch('routers.wallet_router.create_wallet_from_username')
    @patch('business_layer.authentication.Authentication.check_if_username_exists')
    def test_send_amount_failure_invalid_amount(self, mock_check_user_exists,
                                                mock_create_wallet, mock_get_current_user):
        # Arrange
        mock_get_current_user.return_value = self.username
        mock_check_user_exists.return_value = True
        mock_create_wallet.return_value.send_amount.side_effect = InvalidAmountException()

        # Act
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post("/wallet/send", params={"receiver": "receiver_user", "amount": 100}, headers=headers)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'detail': 'Invalid amount entered! Please enter positive amount'})

    @patch('tokens.tokens.get_current_user')
    @patch('routers.wallet_router.create_wallet_from_username')
    @patch('business_layer.authentication.Authentication.check_if_username_exists')
    def test_send_amount_failure_low_balance(self, mock_check_user_exists,
                                             mock_create_wallet, mock_get_current_user):
        # Arrange
        mock_get_current_user.return_value = self.username
        mock_check_user_exists.return_value = True
        mock_create_wallet.return_value.send_amount.side_effect = LowBalanceException()

        # Act
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post("/wallet/send", params={"receiver": "receiver_user", "amount": 100}, headers=headers)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'User wallet balance is low for the transaction'})

    @patch('tokens.tokens.get_current_user')
    @patch('routers.wallet_router.create_wallet_from_username')
    @patch('business_layer.authentication.Authentication.check_if_username_exists')
    def test_send_amount_failure_server_failure(self, mock_check_user_exists,
                                                mock_create_wallet, mock_get_current_user):
        # Arrange
        mock_get_current_user.return_value = self.username
        mock_check_user_exists.return_value = True
        mock_create_wallet.return_value.send_amount.side_effect = DatabaseException()

        # Act
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.post("/wallet/send", params={"receiver": "receiver_user", "amount": 100}, headers=headers)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json(), {'detail': 'Internal Server Error'})

    @patch('tokens.tokens.get_current_user')
    def test_get_wallet_balance_invalid_token(self,
                                              mock_get_current_user
                                              ):
        #Arrange
        mock_get_current_user.return_value = None

        #Act
        headers = {"Authorization": f"Bearer {'ab.bc.cd'}"}
        response = client.get("/wallet/balance", params={"username": self.username}, headers=headers)

        #Assert
        self.assertEqual(response.status_code, 401)
        self.assertRaises(HTTPException)

    @patch('routers.wallet_router.create_wallet_from_username')
    @patch('tokens.tokens.get_current_user')
    def test_get_wallet_balance_success(self, mock_get_current_user,
                                        mock_create_wallet,
                                        ):
        # Arrange
        mock_create_wallet.return_value.get_balance.return_value = 100
        mock_get_current_user.return_value = self.username

        # Act
        headers = {"Authorization": f"Bearer {self.token}"}
        response = client.get("/wallet/balance", params={"username": self.username}, headers=headers)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 100)


if __name__ == '__main__':
    unittest.main()
