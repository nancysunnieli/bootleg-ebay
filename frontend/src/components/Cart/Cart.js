import { useCallback, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import { useDispatch, useSelector } from "react-redux";
import { checkOut, deleteItemFromCart, getItemsFromCart } from "../../slices/cart";
import { getPaymentCard, getPaymentCardByUserID } from "../../slices/payments";
import CartItem from "./CartItem";
const Cart = () => {
    const { cartItems } = useSelector((state) => state.cart);
    const { paymentCard, getPaymentCardLoading } = useSelector((state) => state.payments);
    const dispatch = useDispatch();
    const { user } = useSelector((state) => state.auth);

    useEffect(() => {
        dispatch(getItemsFromCart({ user_id: user.user_id }));
        dispatch(getPaymentCardByUserID({ user_id: user.user_id }));
    }, []);

    const handleDeleteItem = useCallback(
        (item) => {
            console.log("handle Delte item", item);
            dispatch(deleteItemFromCart({ item, user_id: user.user_id }));
        },
        [dispatch]
    );
    console.log("CartItems", cartItems);
    let cartItemCards = cartItems.map((item, i) => (
        <Row key={i} className="mb-3">
            <Col>
                <CartItem key={i} item={item} handleDeleteItem={handleDeleteItem} />
            </Col>
        </Row>
    ));

    const totalPrice = cartItems.reduce(
        (acc, cur) => acc + parseFloat(cur.item.item_price) + parseFloat(cur.item.shipping_price),
        0
    );

    const handlePay = useCallback(() => {
        dispatch(checkOut({ user_id: user.user_id }));
    }, [dispatch]);
    return (
        <div>
            <h1>Cart</h1>
            <Row>
                <Col xl={8}>{cartItemCards}</Col>
                <Col xl={4}>
                    <Card>
                        <Card.Header>Checkout</Card.Header>
                        <Card.Body>
                            <Card.Title>Items: {cartItems.length}</Card.Title>
                            <Card.Text>Total: ${totalPrice}</Card.Text>
                            <div className="d-grid">
                                <Button
                                    size="lg"
                                    disabled={totalPrice === 0 || paymentCard == null}
                                    onClick={handlePay}
                                >
                                    Pay
                                </Button>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Cart;
