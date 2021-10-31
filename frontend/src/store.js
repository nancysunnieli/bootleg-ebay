import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/auth.js";
import itemsReducer from "./slices/items";

const reducer = {
  auth: authReducer,
  items: itemsReducer,
};

const store = configureStore({
  reducer: reducer,
  devTools: true,
});

export default store;
