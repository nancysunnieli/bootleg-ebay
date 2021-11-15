import { useCallback, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAllItems } from "../../slices/items";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import { addItemToCart, deleteItemFromCart, getItemsFromCart } from "../../slices/cart";
import CartItem from "./CartItem";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
const Cart = () => {
    const { cartItems } = useSelector((state) => state.cart);
    const dispatch = useDispatch();
    const getCartItems = () => {
        dispatch(getItemsFromCart());
    };
    const { user } = useSelector((state) => state.auth);

    useEffect(() => {
        getCartItems();
    }, []);

    const handleDeleteItem = useCallback(
        (item) => {
            console.log("handle Delte item", item);
            dispatch(deleteItemFromCart({ item, user_id: user.user_id }));
        },
        [dispatch]
    );

    console.log("cartItems", cartItems);
    let cartItemCards = cartItems.map((item, i) => (
        <Row key={i} className="mb-3">
            <Col>
                <CartItem key={i} item={item} handleDeleteItem={handleDeleteItem} />
            </Col>
        </Row>
    ));

    const totalPrice = cartItems.reduce((acc, cur) => acc + parseFloat(cur.item.price), 0);
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
                                <Button size="lg">Pay</Button>
                            </div>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Cart;
