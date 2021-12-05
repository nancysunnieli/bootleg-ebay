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
import DateTimePicker from "react-datetime-picker";
import { createAuction } from "../../slices/auctions";
const CreateAuctionModal = ({ show, handleClose }) => {
    const { item } = useSelector((state) => state.items);
    const { user } = useSelector((state) => state.auth);

    const [start_time, setStartTime] = useState("");
    const [end_time, setEndTime] = useState("");
    const [shipping, setShipping] = useState("");
    const [buy_now, setBuyNow] = useState(false);
    const [buy_now_price, setBuyNowPrice] = useState("");
    const [starting_price, setStartingPrice] = useState("");

    const dispatch = useDispatch();
    const history = useHistory();
    const close = () => {
        handleClose();
    };

    const handleSave = () => {
        dispatch(
            createAuction({
                start_time: start_time.getTime() / 1000,
                end_time: end_time.getTime() / 1000,
                item_id: item.item._id,
                seller_id: user.user_id,
                bids: [],
                shipping: parseInt(shipping),
                buy_now,
                buy_now_price: parseInt(buy_now_price) || 100000000000000,
                starting_price: parseInt(starting_price),
                history,
            })
        );
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Create Item Auction</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3">
                        <Row>
                            <Form.Label>
                                Start Time<span style={{ color: "red" }}>*</span>
                            </Form.Label>
                        </Row>
                        <Row>
                            <DateTimePicker onChange={setStartTime} value={start_time} />
                        </Row>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Row>
                            <Form.Label>
                                End Time<span style={{ color: "red" }}>*</span>
                            </Form.Label>
                        </Row>
                        <Row>
                            <DateTimePicker onChange={setEndTime} value={end_time} />
                        </Row>
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>
                            Shipping Fee<span style={{ color: "red" }}>*</span>
                        </Form.Label>
                        <Form.Control onChange={(e) => setShipping(e.target.value)} />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>
                            Buy Now?<span style={{ color: "red" }}>*</span>
                        </Form.Label>
                        <Form.Check type="checkbox" onChange={(e) => setBuyNow(e.target.checked)} />
                    </Form.Group>
                    {buy_now && (
                        <Form.Group className="mb-3">
                            <Form.Label>Buy Now Price</Form.Label>
                            <Form.Control onChange={(e) => setBuyNowPrice(e.target.value)} />
                        </Form.Group>
                    )}
                    <Form.Group className="mb-3">
                        <Form.Label>
                            Bid Starting Price<span style={{ color: "red" }}>*</span>
                        </Form.Label>
                        <Form.Control onChange={(e) => setStartingPrice(e.target.value)} />
                    </Form.Group>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={close}>
                    Close
                </Button>
                <Button variant="success" onClick={handleSave}>
                    Create
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default CreateAuctionModal;
