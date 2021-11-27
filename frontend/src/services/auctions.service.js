import axios from "axios";
import { API_URL } from "../config";
const getCurrentAuctions = async () => {
    const resp = await axios.get(API_URL + "auctions/current_auctions");

    console.log("auctions", resp.data);
    return resp.data;
};

const getAuction = async (auction_id) => {
    const resp = await axios.get(API_URL + `auctions/auction/${auction_id}`);
    return resp.data;
};

const getAuctionByItemID = async (item_id) => {
    const resp = await axios.get(API_URL + `auctions/auctions_by_item/${item_id}`);
    return resp.data;
};

const getAuctionMetrics = async (start, end) => {
    const resp = await axios.post(API_URL + `auctions/auction_metrics`, { start, end });
    return resp.data;
};

const removeAuction = async (auction_id) => {
    const resp = await axios.delete(API_URL + `auctions/${auction_id}`);
    return resp.data;
};

const getUserBids = async (user_id) => {
    const resp = await axios.get(API_URL + `auctions/bids/${user_id}`);
    return resp.data;
};

const createBid = async (buyer_id, auction_id, price) => {
    console.log("Create", buyer_id, auction_id, price);
    const resp = await axios.post(API_URL + `auctions/bid`, { buyer_id, auction_id, price });
    return resp.data;
};

const createAuction = async (
    start_time,
    end_time,
    item_id,
    seller_id,
    bids,
    shipping,
    buy_now,
    buy_now_price,
    starting_price
) => {
    const resp = await axios.post(API_URL + "auctions/auction", {
        start_time,
        end_time,
        item_id,
        seller_id,
        bids,
        shipping,
        buy_now,
        buy_now_price,
        starting_price,
    });
    return resp.data;
};

const AuctionsService = {
    getCurrentAuctions,
    getAuction,
    getAuctionByItemID,
    getAuctionMetrics,
    removeAuction,
    getUserBids,
    createBid,
    createAuction,
};

export default AuctionsService;
