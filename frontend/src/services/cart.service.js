import axios from "axios";
import { API_URL } from "../config";

const addItemToCart = async (user_id, item_id) => {
    const response = await axios.post(API_URL + `items/addition/${user_id}`, { item_id });
    console.log("response", response);
    return response.data;
};

const deleteItemFromCart = async (user_id, item_id) => {
    const response = await axios.post(API_URL + `items/removal/${user_id}`, { item_id });
    console.log("response", response);
    return response.data;
};

const getItemsFromCart = async (user_id) => {
    const response = await axios.post(API_URL + `items/cart/${user_id}`, {});
    console.log("response", response);
    return response.data;
};

const emptyCart = async (user_id) => {
    const response = await axios.post(API_URL + `items/empty/${user_id}`, {});
    console.log("response", response);
    return response.data;
};

const checkOut = async (user_id) => {
    const response = await axios.post(API_URL + `items/checkout/${user_id}`, {});
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
