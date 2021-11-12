import axios from "axios";
import { API_URL } from "../config";
const getCurrentAuctions = async () => {
    const resp = await axios.get(API_URL + "/auctions/current_auctions");

    console.log("auctions", resp.data);
    return resp.data;
};

const getAuction = async (auction_id) => {
    const resp = await axios.get(API_URL + `/auctions/auction/${auction_id}`);
    return resp.data;
};

const getAuctionByItemID = async (item_id) => {
    const resp = await axios.get(API_URL + `/auctions/auctions_by_item/${item_id}`);
    return resp.data;
};

const getAuctionMetrics = async (start, end) => {
    const resp = await axios.post(API_URL + `/auctions/auction_metrics`, { start, end });
    return resp.data;
};

const removeAuction = async (auction_id) => {
    const resp = axios.delete(API_URL + `/auctions/${auction_id}`);
    return resp.data;
};

const getUserBids = async (user_id) => {
    const resp = axios.get(API_URL + `/auctions/bids`);
    return resp.data;
};

const AuctionsService = {
    getCurrentAuctions,
    getAuction,
};

export default AuctionsService;
