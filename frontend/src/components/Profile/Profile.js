import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/esm/Container";
import { useDispatch, useSelector } from "react-redux";
import Card from "react-bootstrap/Card";
import EditModalInfo from "./EditInfoModal";
import { useState } from "react";
import { setEditModalVisible } from "../../slices/profile";

const Profile = () => {
    const { user } = useSelector((state) => state.auth);
    const editModalVisible = useSelector((state) => state.profile.visible);
    const dispatch = useDispatch();
    const setShowEditModal = (visibility) => dispatch(setEditModalVisible(visibility));

    const handleDelete = () => {
        window.alert("TODO");
    };

    const handleSuspend = () => {
        window.alert("TODO");
    };

    return (
        <div>
            <Container>
                <h1>Profile</h1>
                <h3>Hello {user.username}!</h3>
                <br />
                <Card>
                    <Card.Body>
                        <Card.Title>Account settings</Card.Title>
                        <Button variant="info" onClick={() => setShowEditModal(true)}>
                            Update Info
                        </Button>{" "}
                        <Button variant="danger" onClick={handleDelete}>
                            Delete
                        </Button>{" "}
                        <Button variant="warning" onClick={handleSuspend}>
                            Suspend
                        </Button>
                    </Card.Body>
                </Card>
                <br />
                <h3>Active Auctions</h3>
            </Container>
            <EditModalInfo show={editModalVisible} handleClose={() => setShowEditModal(false)} />
        </div>
    );
};

export default Profile;
