import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { toast } from "react-toastify";

import AuctionsService from "../services/auctions.service";
import ItemsService from "../services/items.service";

export const getCurrentAuctions = createAsyncThunk(
    "auctions/getCurrentAuctions",
    async (_, thunkAPI) => {
        try {
            const auctions = await AuctionsService.getCurrentAuctions();
            const auctionItems = await Promise.all(
                auctions.map(async (auction) => {
                    let item = await ItemsService.getItem(auction.item_id);
                    return {
                        item,
                        auction,
                    };
                })
            );
            await new Promise((resolve, reject) => {
                setTimeout(resolve, 1000);
            });
            return auctionItems;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getAuction = createAsyncThunk(
    "auctions/getAuction",
    async ({ auction_id }, thunkAPI) => {
        try {
            const auction = await AuctionsService.getAuction(auction_id);
            const item = await ItemsService.getItem(auction.item_id);
            console.log("Auction", auction_id, auction, item);
            return {
                auction,
                item,
            };
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getAuctionBids = createAsyncThunk(
    "auctions/getAuctionBids",
    async ({ auction_id }, thunkAPI) => {
        try {
            const auction = await AuctionsService.getAuction(auction_id);
            return auction.bids;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getAuctionByItemID = createAsyncThunk(
    "auctions/getAuctionByItemID",
    async ({ item_id }, thunkAPI) => {
        try {
            const auction = await AuctionsService.getAuctionByItemID(item_id);
            const item = await ItemsService.getItem(auction.item_id);
            return {
                auction,
                item,
            };
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getAuctionMetrics = createAsyncThunk(
    "auctions/getAuctionMetrics",
    async ({ start, end }, thunkAPI) => {
        try {
            const data = await AuctionsService.getAuctionMetrics(start, end);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const removeAuction = createAsyncThunk(
    "auctions/removeAuction",
    async ({ auction_id }, thunkAPI) => {
        try {
            const data = await AuctionsService.removeAuction(auction_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getUserBids = createAsyncThunk(
    "auctions/getUserBids",
    async ({ user_id }, thunkAPI) => {
        try {
            const data = await AuctionsService.getUserBids(user_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const createBid = createAsyncThunk(
    "auctions/createBid",
    async ({ buyer_id, auction_id, price }, thunkAPI) => {
        try {
            console.log("Creating bid", buyer_id, auction_id, price, parseFloat(price));
            const data = await AuctionsService.createBid(buyer_id, auction_id, parseFloat(price));
            console.log("Created bid", data);
            return data;
        } catch (error) {
            const message = error.toString();
            console.log("Error found", error);
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const initialState = {
    auctions: [],
    auction: null,
    isBidding: false,
    getAuctionLoading: true,
};

const auctionsSlice = createSlice({
    name: "auctions",
    initialState,
    reducers: {
        clearAuction: (state, action) => {
            state.auction = null;
        },
    },
    extraReducers: {
        [getCurrentAuctions.fulfilled]: (state, action) => {
            state.auctions = action.payload;
        },
        [getCurrentAuctions.rejected]: (state, action) => {},
        [getAuction.pending]: (state, action) => {
            state.getAuctionLoading = true;
        },
        [getAuction.fulfilled]: (state, action) => {
            state.getAuctionLoading = false;
            state.auction = action.payload;
        },
        [getAuction.rejected]: (state, action) => {
            state.getAuctionLoading = false;
            toast.error(`Unable to fetch auction ${action.payload}`);
        },
        [getAuctionBids.fulfilled]: (state, action) => {
            state.auction.auction.bids = action.payload;
            const newAuction = { ...state.auction };
            newAuction.auction.bids = action.payload;
            state.auction = newAuction;
        },
        [createBid.pending]: (state, action) => {
            state.isBidding = true;
        },
        [createBid.fulfilled]: (state, action) => {
            state.isBidding = false;
            console.log("action", action);
            toast.success("Succesfully created bid");
        },
        [createBid.rejected]: (state, action) => {
            state.isBdding = false;
            console.log("Create bid failed", action);
            toast.error(`Failed to create bid ${action.payload}`);
        },
    },
});

const { reducer } = auctionsSlice;
export const { clearAuction } = auctionsSlice.actions;
export default reducer;
