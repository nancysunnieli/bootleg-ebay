import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { toast } from "react-toastify";
import AuctionsService from "../services/auctions.service";

import ItemsService from "../services/items.service";

export const getAllItems = createAsyncThunk("items/getAllItems", async (limit, thunkAPI) => {
    try {
        const data = await ItemsService.getAllItems(limit);
        return data;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const getItem = createAsyncThunk("items/getItem", async ({ item_id }, thunkAPI) => {
    try {
        const data = await ItemsService.getItem(item_id);
        let itemAuction;
        try {
            itemAuction = await AuctionsService.getAuctionByItemID(item_id);
        } catch (error) {
            itemAuction = [];
        }

        return { item: data, auction: itemAuction };
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const getFlaggedItems = createAsyncThunk(
    "items/getFlaggedItems",
    async ({ limit }, thunkAPI) => {
        try {
            const data = await ItemsService.getFlaggedItems(limit);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const searchItem = createAsyncThunk(
    "items/searchItem",
    async ({ keywords, category }, thunkAPI) => {
        try {
            const data = await ItemsService.searchItem(keywords, category);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const addUserToWatchlist = createAsyncThunk(
    "items/addUserToWatchlist",
    async ({ user_id, item_id }, thunkAPI) => {
        try {
            const data = await ItemsService.addUserToWatchlist(user_id, item_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const removeItem = createAsyncThunk(
    "items/removeItem",
    async ({ item_id, history }, thunkAPI) => {
        try {
            const data = await ItemsService.removeItem(item_id);
            history.push("/home");
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const reportItem = createAsyncThunk(
    "items/reportItem",
    async ({ item_id, reason }, thunkAPI) => {
        try {
            const data = await ItemsService.reportItem(item_id, reason);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const modifyItem = createAsyncThunk(
    "items/modifyItem",
    async (
        { item_id, name, description, category, photos, sellerID, quantity, history },
        thunkAPI
    ) => {
        try {
            const data = await ItemsService.modifyItem(
                item_id,
                name,
                description,
                category,
                photos,
                sellerID,
                quantity
            );
            history.go(0);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getCategories = createAsyncThunk("items/getCategories", async (_, thunkAPI) => {
    try {
        const data = await ItemsService.getCategories();
        return data;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const addCategory = createAsyncThunk("items/addCategory", async ({ category }, thunkAPI) => {
    try {
        const data = await ItemsService.addCategory(category);
        console.log("Data", data);
        return data;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const removeCategory = createAsyncThunk(
    "items/removeCategory",
    async ({ category }, thunkAPI) => {
        try {
            const data = await ItemsService.removeCategory(category);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const createItem = createAsyncThunk(
    "items/createItem",
    async ({ name, description, category, photos, sellerID, quantity, history }, thunkAPI) => {
        try {
            const data = await ItemsService.createItem(
                name,
                description,
                category,
                photos,
                sellerID,
                quantity
            );
            console.log("uploaded", data, history);
            history.push(`/items/${data._id}`);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getItemsBySeller = createAsyncThunk(
    "items/getItemsBySeller",
    async ({ seller_id }, thunkAPI) => {
        try {
            console.log("seler", seller_id);
            const data = await ItemsService.getItemsBySeller(seller_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const initialState = {
    items: [],
    item: null,
    isGetItemLoading: true,
    flaggedItems: [],
    isGetFlaggedItemsLoading: true,
    isSearchItemLoading: true,
    searchItems: [],
    categories: [],
    isGetCategoriesLoading: true,
    sellerItems: [],
    isGetSellerItemsLoading: true,
};

const itemsSlice = createSlice({
    name: "items",
    initialState,
    reducers: {
        clearItem: (state, action) => {
            state.item = null;
        },
        resetSearchItems: (state, action) => {
            state.searchItems = [];
        },
    },
    extraReducers: {
        [getAllItems.fulfilled]: (state, action) => {
            state.items = action.payload;
        },
        [getAllItems.rejected]: (state, action) => {
            toast.error("Error on retrieving all items " + action.payload);
        },
        [getItem.pending]: (state, action) => {
            state.isGetItemLoading = true;
        },
        [getItem.fulfilled]: (state, action) => {
            state.item = action.payload;
            state.isGetItemLoading = false;
        },
        [getItem.rejected]: (state, action) => {
            state.item = null;
            state.isGetItemLoading = false;
            toast.error("Error on retrieving item" + action.payload);
        },
        [getFlaggedItems.pending]: (state, action) => {
            state.isGetFlaggedItemsLoading = true;
        },
        [getFlaggedItems.fulfilled]: (state, action) => {
            state.isGetFlaggedItemsLoading = false;
            state.flaggedItems = action.payload;
        },
        [getFlaggedItems.rejected]: (state, action) => {
            state.isFgetFlaggedItemsLoading = false;
            toast.error("Error on getting flagged items " + action.payload);
        },
        [searchItem.pending]: (state, action) => {
            state.isSearchItemLoading = true;
        },
        [searchItem.fulfilled]: (state, action) => {
            state.isSearchItemLoading = false;
            state.searchItems = action.payload;
        },
        [searchItem.rejected]: (state, action) => {
            state.isSearchItemLoading = false;
            state.searchItems = [];
            toast.error("Error on getting search items " + action.payload);
        },
        [addUserToWatchlist.pending]: (state, action) => {
            toast("Adding item to watchlist..");
        },
        [addUserToWatchlist.rejected]: (state, action) => {
            toast.error("Erorr on adding item to watchlist " + action.payload);
        },
        [addUserToWatchlist.fulfilled]: (state, action) => {
            toast.success("Succesfully added item to watchlist");
        },
        [removeItem.pending]: (state, action) => {
            toast("Removing item...");
        },
        [removeItem.fulfilled]: (state, action) => {
            toast.success("Succesfully removed item");
        },
        [removeItem.rejected]: (state, action) => {
            toast.error("Error on removing Item " + action.payload);
        },
        [reportItem.fulfilled]: (state, action) => {
            toast.success("Succesfully reported item");
        },
        [reportItem.rejected]: (state, action) => {
            toast.error("Error on reporting itme Item " + action.payload);
        },
        [reportItem.pending]: (state, action) => {
            toast("Reporting item...");
        },
        [modifyItem.pending]: (state, action) => {
            toast("Updating item...");
        },
        [modifyItem.fulfilled]: (state, action) => {
            toast.success("Succesfully updated item");
            // state.item = action.payload;
        },
        [modifyItem.rejected]: (state, action) => {
            toast.error("Error on modifying item " + action.payload);
        },
        [getCategories.fulfilled]: (state, action) => {
            state.isGetCategoriesLoading = false;
            state.categories = action.payload;
        },
        [getCategories.pending]: (state, action) => {
            state.isGetCategoriesLoading = true;
        },
        [getCategories.rejected]: (state, action) => {
            state.isGetCategoriesLoading = false;
            toast.error("Error on retrieving categories " + action.payload);
        },
        [addCategory.fulfilled]: (state, action) => {
            state.categories.push(action.meta.arg.category);
            toast.success("Succesfully added category");
        },
        [addCategory.rejected]: (state, action) => {
            toast.error(`Error, the category ${action.meta.arg.category} already exists`);
        },
        [removeCategory.fulfilled]: (state, action) => {
            // TODO: Check me
            // state.categories = action.payload
            toast.success("Successfully removed category");
        },
        [removeCategory.rejected]: (state, action) => {
            toast.error("Error on removing category " + action.payload);
        },
        [createItem.pending]: (state, action) => {
            toast("Creating item...");
        },
        [createItem.fulfilled]: (state, action) => {
            toast.success("Succesfully created item");
        },
        [createItem.rejected]: (state, action) => {
            toast.error("Error on creating item " + action.payload);
        },
        [getItemsBySeller.pending]: (state, action) => {
            state.isGetSellerItemsLoading = true;
            state.sellerItems = [];
        },
        [getItemsBySeller.fulfilled]: (state, action) => {
            console.log("Fulfilled", action.payload);
            state.isGetSellerItemsLoading = false;
            state.sellerItems = action.payload;
        },
        [getItemsBySeller.rejected]: (state, action) => {
            state.isGetSellerItemsLoading = false;
            toast.error("Unable to get seller items " + action.payload);
        },
    },
});

export const { clearItem, resetSearchItems } = itemsSlice.actions;

const { reducer } = itemsSlice;
export default reducer;
