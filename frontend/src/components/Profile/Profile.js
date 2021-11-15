import { useEffect } from "react";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/esm/Container";
import { useDispatch, useSelector } from "react-redux";
import {
    getPaymentCardByUserID,
    paymentsDeleteAccount,
    setCardModalVisible,
} from "../../slices/payments";
import { deleteAccount, setEditModalVisible, suspendAccount } from "../../slices/profile";
import Loading from "../Loading/Loading";
import EditModalInfo from "./EditInfoModal";
import AddCardModal from "./AddCardModal";

const Profile = () => {
    const { user } = useSelector((state) => state.auth);
    const { paymentCard, getPaymentCardLoading, cardModalVisible } = useSelector(
        (state) => state.payments
    );
    const editModalVisible = useSelector((state) => state.profile.visible);
    const dispatch = useDispatch();
    const setShowEditModal = (visibility) => dispatch(setEditModalVisible(visibility));
    const setShowCardModal = (visibility) => dispatch(setCardModalVisible(visibility));

    useEffect(() => {
        dispatch(getPaymentCardByUserID({ user_id: user.user_id }));
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

    return (
        <div>
            <div>
                <h1>Profile</h1>
                <h3>Hi {user.username}!</h3>
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
                <h2>Your transactions</h2>
            </div>
            <EditModalInfo show={editModalVisible} handleClose={() => setShowEditModal(false)} />
            <AddCardModal show={cardModalVisible} handleClose={() => setShowCardModal(false)} />
        </div>
    );
};

export default Profile;
