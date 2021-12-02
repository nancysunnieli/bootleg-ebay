import { useEffect } from "react";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/esm/Container";
import { useDispatch, useSelector } from "react-redux";
import {
    getPaymentCardByUserID,
    getTransationsByUserId,
    paymentsDeleteAccount,
    setCardModalVisible,
} from "../../slices/payments";
import { deleteAccount, setEditModalVisible, suspendAccount } from "../../slices/profile";
import Loading from "../Loading/Loading";
import EditModalInfo from "./EditInfoModal";
import AddCardModal from "./AddCardModal";
import Table from "react-bootstrap/Table";
import { useHistory } from "react-router-dom";

const Profile = () => {
    const { user } = useSelector((state) => state.auth);
    const {
        paymentCard,
        getPaymentCardLoading,
        cardModalVisible,
        getTransactionsLoading,
        transactions,
    } = useSelector((state) => state.payments);
    const editModalVisible = useSelector((state) => state.profile.visible);
    const dispatch = useDispatch();
    const setShowEditModal = (visibility) => dispatch(setEditModalVisible(visibility));
    const setShowCardModal = (visibility) => dispatch(setCardModalVisible(visibility));
    const history = useHistory();
    useEffect(() => {
        dispatch(getPaymentCardByUserID({ user_id: user.user_id }));
        dispatch(getTransationsByUserId({ user_id: user.user_id }));
    }, []);

    const handleDelete = () => {
        dispatch(deleteAccount(user.user_id));
    };

    const handleSuspend = () => {
        dispatch(suspendAccount({ id: user.user_id, suspended: user.suspended === 0 ? 1 : 0 }));
    };

    const handlePaymentDelete = () => {
        dispatch(paymentsDeleteAccount({ payment_id: paymentCard.payment_id }));
    };

    const renderPaymentCard = () => (
        <Card>
            {paymentCard == null ? (
                <Button onClick={() => setShowCardModal(true)}>Add a Payment Card</Button>
            ) : (
                <Card.Body>
                    <Card.Title>Card</Card.Title>
                    <Card.Text>Card number: {paymentCard.card_number}</Card.Text>
                    <Button variant="danger" onClick={handlePaymentDelete}>
                        Delete
                    </Button>
                </Card.Body>
            )}
        </Card>
    );

    const renderTransactions = () => {
        if (getTransactionsLoading) {
            return <Loading />;
        } else {
            return (
                <Table striped hover responsive="sm">
                    <thead>
                        <tr>
                            <th>Item Name</th>
                            <th>Total Cost</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {transactions.map((transaction, i) => (
                            <tr key={i}>
                                <td>{transaction.item.name}</td>
                                <td>{transaction.money}</td>
                                <td>
                                    <Button
                                        onClick={() =>
                                            history.push(`/items/${transaction.item_id}`)
                                        }
                                    >
                                        View
                                    </Button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            );
        }
    };

    console.log("Transactions", transactions);

    return (
        <div>
            <div>
                <h1>Profile</h1>
                <h3>Hi {user.username}!</h3>
                <h4>Your rating: 5.0★</h4>
                <br />
                <Card>
                    <Card.Body>
                        <Card.Title>Account settings</Card.Title>
                        <Card.Text>Email: {user.email}</Card.Text>
                        <Card.Text>Suspended: {user.suspended === 0 ? "No" : "Yes"}</Card.Text>
                        <Button variant="info" onClick={() => setShowEditModal(true)}>
                            Update Info
                        </Button>{" "}
                        <Button variant="danger" onClick={handleDelete}>
                            Delete
                        </Button>{" "}
                        <Button variant="warning" onClick={handleSuspend}>
                            {user.suspended === 0 ? "Suspend" : "Unsuspend"}
                        </Button>
                    </Card.Body>
                </Card>
                <br />
                <h2>Payment settings</h2>
                {getPaymentCardLoading ? <Loading /> : renderPaymentCard()}
                <br />
                <h2>Your Transactions</h2>
                {getTransactionsLoading ? <Loading /> : renderTransactions()}
            </div>
            <EditModalInfo show={editModalVisible} handleClose={() => setShowEditModal(false)} />
            <AddCardModal show={cardModalVisible} handleClose={() => setShowCardModal(false)} />
        </div>
    );
};

export default Profile;
