import axios from "axios";
import { API_URL } from "../config";
import allItemsMock from "../mocks/all_items.mock.json";
const getAllItems = async (limit) => {
    return allItemsMock;
    // const resp = await axios.post(API_URL + "/items/all_items", { limit });
    // return resp.data;
};

const ItemsService = {
    getAllItems,
};

export default ItemsService;
