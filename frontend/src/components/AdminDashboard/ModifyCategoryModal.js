import { useState } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";
import { useDispatch } from "react-redux";
import { addCategory, removeCategory } from "../../slices/items";

const ModifyCategoryModal = ({ show, handleClose, category }) => {
    const [modifiedCategory, setModifiedCategory] = useState(category);
    const dispatch = useDispatch();

    const close = () => {
        setModifiedCategory(category);
        handleClose();
    };

    const handleSave = () => {
        dispatch(addCategory({ category: modifiedCategory }));
        dispatch(removeCategory({ category }));
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Modify Category</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Control
                        onChange={(e) => setModifiedCategory(e.target.value)}
                        defaultValue={category}
                    />
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={close}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleSave}>
                    Save
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default ModifyCategoryModal;
