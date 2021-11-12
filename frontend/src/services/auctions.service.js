import axios from "axios";
import { API_URL } from "../config";
const getCurrentAuctions = async () => {
    const resp = await axios.get(API_URL + "/auctions/current_auctions");
    console.log("auctions", resp.data);
    return resp.data;
};

const AuctionsService = {
    getCurrentAuctions,
};

export default AuctionsService;
