import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { modifyProfile } from "../../slices/profile";
import CreditCardInput from "react-credit-card-input";
import { createPaymentCard } from "../../slices/payments";
import moment from "moment";
import { addCategory } from "../../slices/items";

const CreateCategoryModal = ({ show, handleClose }) => {
    const { categories } = useSelector((state) => state.items);
    const [category, setCategory] = useState("");

    const dispatch = useDispatch();

    const close = () => {
        setCategory("");
        handleClose();
    };

    const handleSave = () => {
        dispatch(
            addCategory({
                category,
            })
        );
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Add Category</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={(e) => e.preventDefault()}>
                    <Form.Control onChange={(e) => setCategory(e.target.value)} />
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

export default CreateCategoryModal;
