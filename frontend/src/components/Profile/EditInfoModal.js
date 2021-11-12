import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { modifyProfile } from "../../slices/profile";

const EditModalInfo = ({ show, handleClose }) => {
    const { user } = useSelector((state) => state.auth);
    const [email, setEmail] = useState(user.email);
    const [password, setPassword] = useState(user.password);
    const dispatch = useDispatch();
    const isSaving = useSelector((state) => state.profile.isSaving);

    const close = () => {
        setEmail(user.email);
        setPassword(user.password);
        handleClose();
    };

    const handleSave = () => {
        console.log("saving");
        dispatch(modifyProfile({ id: user.user_id, email, password }));
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Edit Profile</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Label>New Email</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Enter new email"
                        value={email}
                        onChange={({ target: { value } }) => setEmail(value)}
                    />
                    <br />
                    <Form.Label>New Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Enter new password"
                        value={password}
                        onChange={({ target: { value } }) => setPassword(value)}
                    />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={close} disabled={isSaving}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleSave} disabled={isSaving}>
                    Save Changes
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default EditModalInfo;
