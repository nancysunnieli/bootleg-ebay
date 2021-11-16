import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { modifyProfile } from "../../slices/profile";
import CreditCardInput from "react-credit-card-input";
import { createPaymentCard } from "../../slices/payments";
import moment from "moment";

const AddCardModal = ({ show, handleClose }) => {
    const { user } = useSelector((state) => state.auth);
    const { paymentCard } = useSelector((state) => state.payments);
    const [card_number, setCardNumber] = useState(paymentCard?.card_number || "");
    const [security_code, setSecurityCode] = useState(paymentCard?.security_code || "");
    const [expiration_date, setExpirationDate] = useState(paymentCard?.expiration_date || "");

    const dispatch = useDispatch();
    const isSaving = useSelector((state) => state.profile.isSaving);

    const close = () => {
        setCardNumber(paymentCard?.card_number || "");
        setSecurityCode(paymentCard?.security_code || "");
        setExpirationDate(paymentCard?.expiration_date || "");
        handleClose();
    };

    const handleSave = () => {
        let expirationDate = moment(expiration_date, "MM / YY").format("YYYY-MM-DD");
        let cardNumber = parseInt(card_number.replace(/\s/g, ""));
        let securityCode = parseInt(security_code);

        dispatch(
            createPaymentCard({
                user_id: user.user_id,
                card_number: cardNumber,
                security_code: securityCode,
                expiration_date: expirationDate,
            })
        );
        handleClose();
    };

    return (
        <Modal show={show} onHide={handleClose}>
            <Modal.Header closeButton>
                <Modal.Title>Edit Profile</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form>
                    <CreditCardInput
                        cardNumberInputProps={{
                            value: card_number,
                            onChange: (e) => setCardNumber(e.target.value),
                        }}
                        cardExpiryInputProps={{
                            value: expiration_date,
                            onChange: (e) => setExpirationDate(e.target.value),
                        }}
                        cardCVCInputProps={{
                            value: security_code,
                            onChange: (e) => setSecurityCode(e.target.value),
                        }}
                        fieldClassName="input"
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

export default AddCardModal;
