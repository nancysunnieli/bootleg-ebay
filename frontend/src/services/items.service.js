import axios from "axios";
import { API_URL } from "../config";
const getAllItems = async (limit) => {
    // return allItemsMock;
    const resp = await axios.post(API_URL + "/items/all_items", { limit });
    console.log("items", resp.data);
    return resp.data;
};

const getItem = async (item_id) => {
    const resp = await axios.post(API_URL + "/items/item", { item_id });
    return resp.data;
};

const ItemsService = {
    getAllItems,
    getItem,
};

export default ItemsService;
