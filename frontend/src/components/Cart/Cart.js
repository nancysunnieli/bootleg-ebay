import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAllItems } from "../../slices/items";
import Row from "react-bootstrap/Row";
import { addItemToCart, getItemsFromCart } from "../../slices/cart";

const Cart = () => {
    const { cartItems } = useSelector((state) => state.cart);
    const dispatch = useDispatch();
    const getCartItems = () => {
        dispatch(getItemsFromCart());
    };

    useEffect(() => {
        getCartItems();
    }, []);

    // let itemCards = items.map((item, i) => <Item key={i} item={item} />);
    // if (itemCards.length == 0) {
    //     itemCards = Array.from(Array(10)).fill(<ItemSkeleton />);
    // }
    console.log(cartItems);
    return (
        <div>
            <h1>Cart</h1>
            <Row xs={1} md={3} className="g-4">
                {/* {itemCards} */}
            </Row>
        </div>
    );
};

export default Cart;
