import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getItemsBySeller } from "../../slices/items";
import Spinner from "react-bootstrap/Spinner";
import { ScrollMenu, VisibilityContext } from "react-horizontal-scrolling-menu";
import ItemCard from "../Items/ItemCard";

const SellerItems = () => {
    const { user } = useSelector((state) => state.auth);
    const { sellerItems, isGetSellerItemsLoading } = useSelector((state) => state.items);
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(getItemsBySeller({ seller_id: user.user_id }));
    }, []);

    if (isGetSellerItemsLoading) {
        return <Spinner animation="grow" variant="success" />;
    }
    return (
        <div style={{ position: "relative" }}>
            <div
                style={{
                    height: "100%",
                    width: "100%",
                    position: "absolute",
                    zIndex: 1000,
                    pointerEvents: "none",
                    background:
                        "-webkit-linear-gradient(left, rgba(255,255,255,0.65) 0%, rgba(255,255,255,0) 10%, rgba(255,255,255,0) 90%,rgba(255,255,255,0.65) 100%)",
                }}
            />
            <ScrollMenu>
                {sellerItems.map((item, index) => (
                    <div key={index} style={{ width: "20vw", marginRight: "1rem" }}>
                        <ItemCard item={item} key={index} />
                    </div>
                ))}
            </ScrollMenu>
        </div>
    );
};

export default SellerItems;
