import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getCurrentAuctions } from "../../slices/auctions";
import AuctionCard from "./AuctionsCard";
import Row from "react-bootstrap/Row";
import ItemSkeleton from "../Items/ItemSkeleton";
import PrivateRoute from "../Routing/PrivateRouter";
import Auction from "./Auction";
import { useRouteMatch } from "react-router-dom";

const Auctions = () => {
    const { auctions } = useSelector((state) => state.auctions);
    const { cartItems } = useSelector((state) => state.cart);
    const { path } = useRouteMatch();

    const dispatch = useDispatch();
    const getAuctions = () => {
        console.log("getauctions");
        dispatch(getCurrentAuctions());
    };

    useEffect(() => {
        getAuctions();
    }, []);

    let auctionCards = auctions.map(({ auction, item }, i) => {
        let isBuyNowDisabled = cartItems.findIndex((c) => c.item._id === item._id) != -1;
        return (
            <AuctionCard
                key={i}
                auction={auction}
                item={item}
                isBuyNowDisabled={isBuyNowDisabled}
            />
        );
    });

    if (auctionCards.length == 0) {
        auctionCards = Array.from(Array(10))
            .fill(0)
            .map((_, i) => <ItemSkeleton key={i} />);
    }
    console.log("path", `${path}/:auction_id`);

    return (
        <div>
            <div>
                <h1>Auctions</h1>
                <h3>Live Auctions</h3>
                <Row xs={1} md={3} className="g-4">
                    {auctionCards}
                </Row>

                <br />
                <h3>Upcoming Auctions</h3>
            </div>
        </div>
    );
};

export default Auctions;
