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

const EditAuctionModal = ({ show, handleClose }) => {
    const { auction, getAuctionLoading } = useSelector((state) => state.auctions);
    console.log("Auction", auction);
    const [shipping, setShipping] = useState(auction.auction.shipping);
    const [buy_now, setBuyNow] = useState(auction.auction.buy_now);
    const [buy_now_price, setBuyNowPrice] = useState(auction.auction.buy_now_price);

    const dispatch = useDispatch();

    const close = () => {
        handleClose();
    };

    const handleSave = () => {
        window.alert("TODO");
        dispatch();
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Edit Auction</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <Form.Group className="mb-3">
                        <Form.Label>Shipping</Form.Label>
                        <Form.Control
                            onChange={(e) => setShipping(e.target.value)}
                            defaultValue={auction.auction.shipping}
                        />
                    </Form.Group>
                    <Form.Group className="mb-3">
                        <Form.Label>Buy Now?</Form.Label>
                        <Form.Check
                            type="checkbox"
                            onChange={(e) => setBuyNow(e.target.checked)}
                            defaultValue={auction.auction.buy_now}
                        />
                    </Form.Group>
                    {buy_now && (
                        <Form.Group className="mb-3">
                            <Form.Label>Buy Now Price</Form.Label>
                            <Form.Control
                                onChange={(e) => setBuyNowPrice(e.target.value)}
                                defaultValue={auction.auction.buy_now_price}
                            />
                        </Form.Group>
                    )}
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

export default EditAuctionModal;
