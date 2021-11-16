import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAllItems } from "../../slices/items";
import ItemCard from "./ItemCard";
import ItemSkeleton from "./ItemSkeleton";
import Row from "react-bootstrap/Row";

const Items = () => {
    const { items } = useSelector((state) => state.items);
    const dispatch = useDispatch();
    const getItems = () => {
        dispatch(getAllItems());
    };

    useEffect(() => {
        getItems();
    }, []);

    let itemCards = items.map((item, i) => <ItemCard key={i} item={item} />);
    if (itemCards.length == 0) {
        itemCards = Array.from(Array(10))
            .fill(0)
            .map((_, i) => <ItemSkeleton key={i} />);
    }
    return (
        <div>
            <h1>Items</h1>
            <Row xs={1} md={3} className="g-4">
                {itemCards}
            </Row>
        </div>
    );
};

export default Items;
