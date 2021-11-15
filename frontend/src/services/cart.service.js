import axios from "axios";
import { API_URL } from "../config";

const addItemToCart = async (user_id, item_id) => {
    console.log("user", user_id, typeof user_id);
    const response = await axios.post(API_URL + `carts/addition`, { item_id, user_id });
    console.log("response", response);
    return response.data;
};

const deleteItemFromCart = async (user_id, item_id) => {
    const response = await axios.post(API_URL + `carts/removal`, { item_id, user_id });
    console.log("response", response);
    return response.data;
};

const getItemsFromCart = async (user_id) => {
    const response = await axios.get(API_URL + `carts/cart/${user_id}`);
    console.log("get items from cart", response);
    return response.data;
};

const emptyCart = async (user_id) => {
    const response = await axios.post(API_URL + `carts/empty`, { user_id });
    console.log("response", response);
    return response.data;
};

const checkOut = async (user_id) => {
    const response = await axios.post(API_URL + `carts/checkout`, { user_id });
    console.log("response", response);
    return response.data;
};

const CartService = {
    addItemToCart,
    deleteItemFromCart,
    getItemsFromCart,
    emptyCart,
    checkOut,
};

export default CartService;
