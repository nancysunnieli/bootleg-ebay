import { useEffect, useRef, useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { useDispatch, useSelector } from "react-redux";
import { createItem, getCategories } from "../../slices/items";
import CreateCategoryModal from "./CreateCategoryModal";
import { useHistory } from "react-router-dom";

export const toBase64 = (file) =>
    new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result.split(",")[1]);
        reader.onerror = (error) => reject(error);
    });

export default function CreateItem() {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [category, setCategory] = useState([]);
    const [photos, setPhotos] = useState("");
    const [photoName, setPhotoName] = useState("");
    const [quantity, setQuantity] = useState("");

    const [modalVisible, setModalVisibile] = useState(false);
    const { categories } = useSelector((state) => state.items);
    const { user } = useSelector((state) => state.auth);
    const inputRef = useRef();
    const history = useHistory();

    const dispatch = useDispatch();
    useEffect(() => {
        dispatch(getCategories());
    }, []);

    const handleSubmit = () => {
        dispatch(
            createItem({
                name,
                description,
                category,
                photos,
                sellerID: user.user_id,
                quantity: parseInt(quantity),
                history,
            })
        );
    };

    const handleImageUpload = () => {
        inputRef.current.click();
    };

    const handleFileSelect = async (e) => {
        let file = e.target.files[0];
        let base64Photo = await toBase64(file);
        setPhotos(base64Photo);
        setPhotoName(file.name);
    };

    return (
        <div>
            <h1>Create Item</h1>
            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>
                        Item Name<span style={{ color: "red" }}>*</span>
                    </Form.Label>
                    <Form.Control onChange={(e) => setName(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>
                        Description<span style={{ color: "red" }}>*</span>
                    </Form.Label>
                    <Form.Control onChange={(e) => setDescription(e.target.value)} />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>
                        Category<span style={{ color: "red" }}>*</span>
                    </Form.Label>
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
                        <Col>
                            <Button onClick={() => setModalVisibile(true)} variant="info">
                                Create new category
                            </Button>
                        </Col>
                    </Row>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Row>
                        <Col xs={1}>
                            <Form.Label>
                                Photos<span style={{ color: "red" }}>*</span>
                            </Form.Label>
                        </Col>
                        <Col md="auto">
                            <p>{photoName}</p>
                        </Col>
                        <Col xs={5}>
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
                    <Form.Label>
                        Quantity<span style={{ color: "red" }}>*</span>
                    </Form.Label>
                    <Form.Control onChange={(e) => setQuantity(e.target.value)} />
                </Form.Group>
                <Button onClick={handleSubmit}>Create</Button>
            </Form>
            <CreateCategoryModal show={modalVisible} handleClose={() => setModalVisibile(false)} />
        </div>
    );
}
