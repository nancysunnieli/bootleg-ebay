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

const getFlaggedItems = async () => {
    const resp = await axios.post(API_URL + "items/flagged_items", {});
    return resp.data;
};

const searchItem = async (keywords, category) => {
    let payload = Object.assign({}, category === null ? null : { category }, { keywords });
    const resp = await axios.post(API_URL + "items/search", payload);
    return resp.data;
};

const addUserToWatchlist = async (user_id, item_id, max_price) => {
    const resp = await axios.post(API_URL + "items/watchlist", { user_id, item_id, max_price });
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

const modifyItem = async (item_id, name, description, category, photos, sellerID, quantity) => {
    let payload = {
        item_id,
        name,
        description,
        category,
        sellerID,
        quantity,
    };
    if (photos != null && photos.length !== 0) {
        payload[photos] = photos;
    }
    const resp = await axios.post(API_URL + "items/modification", payload);
    return resp.data;
};

const createItem = async (name, description, category, photos, sellerID, quantity) => {
    const resp = await axios.post(API_URL + "items/addition", {
        name,
        description,
        category,
        photos,
        sellerID,
        quantity,
    });
    return resp.data;
};

// TODO: Not sure why this is needed
// const editItemCategories = async () => {};
// const modifyItemQuantity = async () => {};

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

const getItemsBySeller = async (seller_id) => {
    const resp = await axios.get(API_URL + `items/items_by_seller/${seller_id}`);
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
    getCategories,
    addCategory,
    removeCategory,
    getItemsBySeller,
};

export default ItemsService;
