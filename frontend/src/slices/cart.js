import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import CartService from "../services/cart.service";
import { toast } from "react-toastify";

const initialState = {
    cartItems: [],
    isLoading: true,
};

export const addItemToCart = createAsyncThunk(
    "cart/addItemToCart",
    async ({ item, user_id }, thunkAPI) => {
        try {
            const data = await CartService.addItemToCart(item.item_id, user_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const deleteItemFromCart = createAsyncThunk(
    "cart/deleteItemFromCart",
    async ({ item, user_id }, thunkAPI) => {
        try {
            const data = await CartService.deleteItemFromCart(item.item_id, user_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getItemsFromCart = createAsyncThunk(
    "cart/getItemsFromCart",
    async ({ user_id }, thunkAPI) => {
        try {
            const data = await CartService.getItemsFromCart(user_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const emptyCart = createAsyncThunk("cart/emptyCart", async ({ user_id }, thunkAPI) => {
    try {
        const data = await CartService.emptyCart(user_id);
        return data;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const checkOut = createAsyncThunk("cart/checkOut", async ({ user_id }, thunkAPI) => {
    try {
        const data = await CartService.checkOut(user_id);
        return data;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

const cartSlice = createSlice({
    name: "card",
    initialState,
    reducers: {},
    extraReducers: {
        [addItemToCart.pending]: (state, action) => {
            state.cartItems.push({ item: action.meta.arg.item, status: "pending" });
        },
        [addItemToCart.fulfilled]: (state, action) => {
            for (let cartItem of state.cartItems) {
                if (cartItem.item._id == action.meta.arg.item._id) {
                    cartItem.status = "success";
                }
            }
            toast("it worked");
        },
        [addItemToCart.rejected]: (state, action) => {
            for (let cartItem of state.cartItems) {
                if (cartItem.item._id == action.meta.arg.item._id) {
                    cartItem.status = "error";
                }
            }
            toast("Wow");
        },
        [deleteItemFromCart.pending]: (state, action) => {
            let itemIndex = state.cartItems.findIndex(
                (item) => item._id == action.meta.arg.item.item_id
            );
            state.cartItems = state.cartItems.splice(itemIndex, 1);
        },
        [deleteItemFromCart.fulfilled]: (state, action) => {},
        [deleteItemFromCart.rejected]: (state, action) => {},
        [getItemsFromCart.pending]: (state, action) => {},
        [getItemsFromCart.fulfilled]: (state, action) => {
            state.cartItems = action.payload.map((item) => ({ item, status: "succes" }));
        },
        [getItemsFromCart.rejected]: (state, action) => {},
        [emptyCart.pending]: (state, action) => {},
        [emptyCart.fulfilled]: (state, action) => {},
        [emptyCart.rejected]: (state, action) => {},
        [checkOut.pending]: (state, action) => {},
        [checkOut.fulfilled]: (state, action) => {},
        [checkOut.rejected]: (state, action) => {},
    },
});
export const {} = cartSlice.actions;

export default cartSlice.reducer;
