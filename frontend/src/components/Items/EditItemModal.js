import { useRef, useState } from "react";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";
import Row from "react-bootstrap/Row";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import { modifyItem } from "../../slices/items";
import { toBase64 } from "./CreateItem";
const EditItemModal = ({ show, handleClose }) => {
    const { item } = useSelector((state) => state.items);
    const { user } = useSelector((state) => state.auth);
    const { categories } = useSelector((state) => state.items);
    const [name, setName] = useState(item.item.name);
    const [description, setDescription] = useState(item.item.description);
    const [category, setCategory] = useState(item.item.category);
    const [photos, setPhotos] = useState("");
    const [photoName, setPhotoName] = useState("");
    const [quantity, setQuantity] = useState(item.item.quantity);

    const dispatch = useDispatch();
    const history = useHistory();
    const inputRef = useRef();

    const close = () => {
        setName(item.item.name);
        setDescription(item.item.description);
        setPhotos("");
        setPhotoName("");
        setQuantity(item.item.quantity);
        handleClose();
    };
    console.log("Category", category);
    const handleSave = () => {
        dispatch(
            modifyItem({
                item_id: item.item._id,
                name,
                description,
                category,
                photos,
                sellerID: user.user_id,
                quantity: parseInt(quantity),
                history,
            })
        );
        handleClose();
    };

    const handleImageUpload = () => {
        inputRef.current.click();
    };

    const handleFileSelect = async (e) => {
        let file = e.target.files[0];
        if (file == null) return;
        let base64Photo = await toBase64(file);
        setPhotos(base64Photo);
        setPhotoName(file.name);
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Edit Item</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3">
                        <Form.Label>Item Name</Form.Label>
                        <Form.Control
                            onChange={(e) => setName(e.target.value)}
                            defaultValue={name}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                            onChange={(e) => setDescription(e.target.value)}
                            defaultValue={description}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Category</Form.Label>
                        <Row>
                            <Col>
                                <Form.Control
                                    as="select"
                                    multiple
                                    value={category}
                                    onChange={(e) =>
                                        setCategory(
                                            [].slice
                                                .call(e.target.selectedOptions)
                                                .map((item) => item.value)
                                                .filter((value) => value !== "Select Category")
                                        )
                                    }
                                >
                                    <option>Select Category</option>
                                    {categories.map((category, i) => (
                                        <option key={i} value={category}>
                                            {category}
                                        </option>
                                    ))}
                                </Form.Control>
                            </Col>
                        </Row>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Row>
                            <Col xs="auto">
                                <Form.Label>Photos</Form.Label>
                            </Col>
                            <Col md="auto">
                                <p>{photoName}</p>
                            </Col>
                            <Col md="auto">
                                <Button variant="info" onClick={handleImageUpload}>
                                    Upload Photo
                                </Button>
                            </Col>
                            <input
                                type="file"
                                hidden
                                ref={inputRef}
                                accept="image/png"
                                onChange={handleFileSelect}
                            />
                        </Row>
                        <Row xs={6}></Row>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Quantity</Form.Label>
                        <Form.Control
                            onChange={(e) => setQuantity(e.target.value)}
                            defaultValue={quantity}
                        />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={close}>
                    Close
                </Button>
                <Button variant="success" onClick={handleSave}>
                    Save
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default EditItemModal;
