import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import CartService from "../services/cart.service";
import { toast } from "react-toastify";
import { current } from "immer";
const initialState = {
    cartItems: [],
    isLoading: true,
};

export const addItemToCart = createAsyncThunk(
    "cart/addItemToCart",
    async ({ item, user_id }, thunkAPI) => {
        try {
            const data = await CartService.addItemToCart(user_id, item._id);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const deleteItemFromCart = createAsyncThunk(
    "cart/deleteItemFromCart",
    async ({ item, user_id }, thunkAPI) => {
        try {
            console.log(item._id, user_id);
            const data = await CartService.deleteItemFromCart(user_id, item._id);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getItemsFromCart = createAsyncThunk(
    "cart/getItemsFromCart",
    async ({ user_id }, thunkAPI) => {
        try {
            const data = await CartService.getItemsFromCart(user_id);
            console.log("GetItemsFromCart", data);
            return data;
        } catch (error) {
            const message = error.response?.data?.message || error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const emptyCart = createAsyncThunk("cart/emptyCart", async ({ user_id }, thunkAPI) => {
    try {
        const data = await CartService.emptyCart(user_id);
        return data;
    } catch (error) {
        const message = error.response?.data?.message || error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const checkOut = createAsyncThunk("cart/checkOut", async ({ user_id }, thunkAPI) => {
    try {
        const data = await CartService.checkOut(user_id);
        return data;
    } catch (error) {
        const message = error.response?.data?.message || error.toString();
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
            toast.success("Succesfully added item to cart");
        },
        [addItemToCart.rejected]: (state, action) => {
            for (let cartItem of state.cartItems) {
                if (cartItem.item._id == action.meta.arg.item._id) {
                    cartItem.status = "error";
                }
            }
            toast.error("Error adding item to cart");
        },
        [deleteItemFromCart.pending]: (state, action) => {
            // console.log("Current item", current(state.cartItems));
            state.cartItems = state.cartItems.filter((item) => {
                return item.item._id !== action.meta.arg.item._id;
            });
        },
        [deleteItemFromCart.fulfilled]: (state, action) => {},
        [deleteItemFromCart.rejected]: (state, action) => {},
        [getItemsFromCart.pending]: (state, action) => {},
        [getItemsFromCart.fulfilled]: (state, action) => {
            state.cartItems = action.payload.map((item) => ({ item, status: "success" }));
        },
        [getItemsFromCart.rejected]: (state, action) => {},
        [emptyCart.pending]: (state, action) => {},
        [emptyCart.fulfilled]: (state, action) => {},
        [emptyCart.rejected]: (state, action) => {},
        [checkOut.pending]: (state, action) => {
            toast("Checking out...");
        },
        [checkOut.fulfilled]: (state, action) => {
            toast.success("Succesfully checked out!");
            state.cartItems = [];
        },
        [checkOut.rejected]: (state, action) => {
            toast.error("Oops, an error occurred while checking out " + action.payload);
        },
    },
});
export const {} = cartSlice.actions;

export default cartSlice.reducer;
