import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";
import { useDispatch } from "react-redux";
import { addCategory, removeCategory } from "../../slices/items";
import { sendEmail } from "../../slices/notifs";

const ReplyModal = ({ show, handleClose, recipient, subject }) => {
    const [body, setBody] = useState("");
    const dispatch = useDispatch();
    const re = /<(.*@.*)>/;
    const email = (recipient.match(re) || {})[1];

    const close = () => {
        setBody(body);
        handleClose();
    };

    const handleSave = () => {
        dispatch(sendEmail({ recipient: email, subject: `Re: ${subject}`, body }));
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Reply to {email}</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Control onChange={(e) => setBody(e.target.value)} />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={close}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleSave}>
                    Send
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default ReplyModal;
