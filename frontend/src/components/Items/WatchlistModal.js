import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { modifyProfile } from "../../slices/profile";
import CreditCardInput from "react-credit-card-input";
import { createPaymentCard } from "../../slices/payments";
import moment from "moment";
import { addCategory, addUserToWatchlist } from "../../slices/items";

const WatchlistModal = ({ show, handleClose }) => {
    const { item } = useSelector((state) => state.items);
    const { user } = useSelector((state) => state.auth);

    const [maxStartingPrice, setMaxStartingPrice] = useState("");

    const dispatch = useDispatch();

    const close = () => {
        setMaxStartingPrice("");
        handleClose();
    };

    const handleSave = () => {
        dispatch(addUserToWatchlist({ user_id: user.user_id, item_id: item.item._id }));
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Add to Watchlist</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Label>Max starting price</Form.Label>
                    <Form.Control onChange={(e) => setMaxStartingPrice(e.target.value)} />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={close}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleSave}>
                    Add
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default WatchlistModal;
