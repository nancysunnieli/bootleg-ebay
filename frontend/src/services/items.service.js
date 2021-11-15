import axios from "axios";
import { API_URL } from "../config";
const getAllItems = async (limit) => {
    // return allItemsMock;
    const resp = await axios.post(API_URL + "items/all_items", { limit });
    console.log("items", resp.data);
    return resp.data;
};

const getItem = async (item_id) => {
    const resp = await axios.post(API_URL + "items/item", { item_id });
    return resp.data;
};

const getFlaggedItems = async (limit) => {
    const resp = await axios.post(API_URL + "items/flagged_items", { limit });
    return resp.data;
};

const searchItem = async (keywords, category) => {
    const resp = await axios.post(API_URL + "items/search", { keywords, category });
    return resp.data;
};

const addUserToWatchlist = async (user_id, item_id) => {
    const resp = await axios.post(API_URL + "items/watchlist", { user_id, item_id });
    return resp.data;
};

const removeItem = async (item_id) => {
    const resp = await axios.post(API_URL + "items/removal", { item_id });
    return resp.data;
};

const reportItem = async (item_id, reason) => {
    const resp = await axios.post(API_URL + "items/report", { item_id, reason });
    return resp.data;
};

const modifyItem = async (
    item_id,
    name,
    description,
    category,
    photos,
    sellerID,
    price,
    quantity,
    shipping
) => {
    const resp = await axios.post(API_URL + "items/modification", {
        item_id,
        name,
        description,
        category,
        photos,
        sellerID,
        price,
        quantity,
        shipping,
    });
    return resp.data;
};

const createItem = async (
    name,
    description,
    category,
    photos,
    sellerID,
    price,
    quantity,
    shipping
) => {
    const resp = await axios.post(API_URL + "items/addition", {
        name,
        description,
        category,
        photos,
        sellerID,
        price,
        quantity,
        shipping,
    });
    return resp.data;
};

// TODO: Not sure why this is needed
const editItemCategories = async () => {};
const modifyItemQuantity = async () => {};

const getCategories = async () => {
    const resp = await axios.get(API_URL + "items/all_categories");
    return resp.data;
};

const addCategory = async (category) => {
    const resp = await axios.post(API_URL + "items/category_addition", { category });
    return resp.data;
};

const removeCategory = async (category) => {
    const resp = await axios.post(API_URL + "items/category_removal", { category });
    return resp.data;
};

const ItemsService = {
    getAllItems,
    getItem,
    getFlaggedItems,
    searchItem,
    addUserToWatchlist,
    removeItem,
    reportItem,
    modifyItem,
    createItem,
    editItemCategories,
    getCategories,
    addCategory,
    removeCategory,
};

export default ItemsService;
