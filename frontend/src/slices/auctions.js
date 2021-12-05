import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { toast } from "react-toastify";

import AuctionsService from "../services/auctions.service";
import ItemsService from "../services/items.service";
import UserService from "../services/user.service";

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
            const message = error.response?.data?.message || error.toString();
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
            console.log("Auction", auction);
            const seller = await UserService.getUserInfo(auction.seller_id);
            return {
                auction: {
                    ...auction,
                    seller_rating: (seller.total_rating / seller.number_of_ratings || 0).toFixed(1),
                },
                item,
            };
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
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
            const message = error.response?.data?.message || error.toString();
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
            const message = error.response?.data?.message || error.toString();
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
            const message = error.response?.data?.message || error.toString();
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
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const modifyAuction = createAsyncThunk(
    "auctions/modifyAuction",
    async ({ auction_id, shipping, buy_now, buy_now_price }, thunkAPI) => {
        try {
            const data = await AuctionsService.modifyAuction(
                auction_id,
                shipping,
                buy_now,
                buy_now_price
            );
            console.log("modify", data);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
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
            const message = error.response?.data?.message || error.toString();
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
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const createAuction = createAsyncThunk(
    "auctions/createAuction",
    async (
        {
            start_time,
            end_time,
            item_id,
            seller_id,
            bids,
            shipping,
            buy_now,
            buy_now_price,
            starting_price,
            history,
        },
        thunkAPI
    ) => {
        try {
            const data = await AuctionsService.createAuction(
                start_time,
                end_time,
                item_id,
                seller_id,
                bids,
                shipping,
                buy_now,
                buy_now_price,
                starting_price
            );
            history.push(`/auctions/${data.auction_id}`);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const stopAuctionEarly = createAsyncThunk(
    "auctions/stopAuctionEarly",
    async (auction_id, thunkAPI) => {
        try {
            const data = await AuctionsService.stopAuctionEarly(auction_id);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.reject(message);
        }
    }
);

const initialState = {
    auctions: [],
    auction: null,
    isBidding: false,
    getAuctionLoading: true,
    getUserBidsLoading: true,
    userBids: [],
    getAuctionMetricsLoading: false,
    auctionMetrics: null,
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
        [getUserBids.pending]: (state, action) => {
            state.getUserBidsLoading = true;
        },
        [getUserBids.fulfilled]: (state, action) => {
            state.getUserBidsLoading = false;
            state.userBids = action.payload;
        },
        [getUserBids.rejected]: (state, action) => {
            state.getUserBidsLoading = false;
            toast.error("Unable to fetch user bids " + action.payload);
        },
        [createAuction.pending]: (state, action) => {
            toast("Creating Auction...");
        },
        [createAuction.fulfilled]: (state, action) => {
            toast.success("Succesfully created auction!");
        },
        [createAuction.rejected]: (state, action) => {
            toast.error("Error creating auction " + action.payload);
        },
        [getAuctionMetrics.pending]: (state, action) => {
            state.getAuctionMetricsLoading = true;
        },
        [getAuctionMetrics.fulfilled]: (state, action) => {
            state.getAuctionMetricsLoading = false;
            state.auctionMetrics = action.payload;
        },
        [getAuctionMetrics.rejected]: (state, action) => {
            state.getAuctionMetricsLoading = false;
            toast.error("Error on fetching auction metrics " + action.payload);
        },
        [modifyAuction.pending]: (state, action) => {
            toast("Modifying auction..");
        },
        [modifyAuction.fulfilled]: (state, action) => {
            toast.success("Succesfully modified auction");
            window.location.reload();
        },
        [modifyAuction.rejected]: (state, action) => {
            toast.error("Error on modifying auction " + action.payload);
        },
        [stopAuctionEarly.pending]: (state, action) => {
            toast("Ending auction early..");
        },
        [stopAuctionEarly.fulfilled]: (state, action) => {
            toast.success("Succesfully ended auction early");
            window.location.reload();
        },
        [stopAuctionEarly.rejected]: (state, action) => {
            toast.error("Error on stop auction early " + action.payload);
        },
    },
});

const { reducer } = auctionsSlice;
export const { clearAuction } = auctionsSlice.actions;
export default reducer;
