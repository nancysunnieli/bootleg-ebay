import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { modifyProfile } from "../../slices/profile";
import { reportItem } from "../../slices/items";

const ReportModal = ({ item_id, show, handleClose }) => {
    const { user } = useSelector((state) => state.auth);
    const [reason, setReason] = useState("");
    const dispatch = useDispatch();

    const close = () => {
        setReason("");
        handleClose();
    };

    const handleSave = () => {
        dispatch(reportItem({ item_id, reason }));
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Report Item</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Label>Reason</Form.Label>
                    <Form.Control
                        placeholder="Enter a reason"
                        value={reason}
                        onChange={({ target: { value } }) => setReason(value)}
                    />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={close}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleSave}>
                    Save Changes
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default ReportModal;
