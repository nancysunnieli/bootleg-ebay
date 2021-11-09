import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import CartService from "../services/cart.service";

const initialState = {
    items: [],
};

export const addItemToCart = createAsyncThunk(
    "cart/addItemToCart",
    async ({ id, item_id }, thunkAPI) => {
        try {
            const data = await CartService.addItemToCart(id, item_id);
            thunkAPI.dispatch(setUser(data));
            return {};
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const modifyProfile = createAsyncThunk(
    "auth/modifyProfile",
    async ({ id, email, password }, thunkAPI) => {
        console.log("Modify profile");
        try {
            const data = await UserService.modifyProfile(id, { email, password });
            thunkAPI.dispatch(setUser(data));
            thunkAPI.dispatch(setEditModalVisible(false));
            return { user: data };
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const deleteAccount = createAsyncThunk("auth/deleteAccount", async (id, thunkAPI) => {
    console.log("Delete account");
    try {
        const result = await UserService.deleteAccount(id);
        window.location.reload();
        return result;
    } catch (error) {
        const message = error.toString();
        return thunkAPI.rejectWithValue(message);
    }
});

export const suspendAccount = createAsyncThunk(
    "auth/suspendAccount",
    async ({ id, suspended }, thunkAPI) => {
        try {
            const data = await UserService.suspendAccount(id, suspended);
            thunkAPI.dispatch(setUser(data));
            return { user: data };
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const profileSlice = createSlice({
    name: "profile",
    initialState,
    reducers: {
        setEditModalVisible(state, action) {
            state.visible = action.payload;
        },
    },
    extraReducers: {
        [modifyProfile.pending]: (state, action) => {
            state.isSaving = true;
        },
        [modifyProfile.fulfilled]: (state, action) => {
            state.isSaving = false;
        },
        [modifyProfile.rejected]: (state, action) => {
            window.alert("oops");
        },
        [deleteAccount.pending]: (state, action) => {},
        [deleteAccount.fulfilled]: (state, action) => {},
        [deleteAccount.rejected]: (state, action) => {
            window.alert("oops");
        },
    },
});
export const { setEditModalVisible } = profileSlice.actions;

export default profileSlice.reducer;
