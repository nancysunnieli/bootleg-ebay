import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/esm/Container";
import { useDispatch, useSelector } from "react-redux";
import { deleteAccount, setEditModalVisible, suspendAccount } from "../../slices/profile";
import EditModalInfo from "./EditInfoModal";

const Profile = () => {
    const { user } = useSelector((state) => state.auth);
    const editModalVisible = useSelector((state) => state.profile.visible);
    const dispatch = useDispatch();
    const setShowEditModal = (visibility) => dispatch(setEditModalVisible(visibility));

    const handleDelete = () => {
        dispatch(deleteAccount(user.user_id));
    };

    const handleSuspend = () => {
        dispatch(suspendAccount({ id: user.user_id, suspended: user.suspended === 0 ? 1 : 0 }));
    };

    return (
        <div>
            <div>
                <h1>Profile</h1>
                <h3>Hello {user.username}!</h3>
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
            </div>
            <EditModalInfo show={editModalVisible} handleClose={() => setShowEditModal(false)} />
        </div>
    );
};

export default Profile;
