import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

import AuctionsService from "../services/auctions.service";
import ItemsService from "../services/items.service";

const initialState = {
    auctions: [],
};

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
            return auctionItems;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const auctionsSlice = createSlice({
    name: "auctions",
    initialState,
    extraReducers: {
        [getCurrentAuctions.fulfilled]: (state, action) => {
            state.auctions = action.payload;
        },
        [getCurrentAuctions.rejected]: (state, action) => {},
    },
});

const { reducer } = auctionsSlice;
export default reducer;
