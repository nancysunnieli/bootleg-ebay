import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getCurrentAuctions } from "../../slices/auctions";
import AuctionCard from "./AuctionCard";
import Row from "react-bootstrap/Row";
import ItemSkeleton from "../Items/ItemSkeleton";

const Auctions = () => {
    const { auctions } = useSelector((state) => state.auctions);
    const dispatch = useDispatch();
    const getAuctions = () => {
        console.log("getauctions");
        dispatch(getCurrentAuctions());
    };

    useEffect(() => {
        getAuctions();
    }, []);

    let auctionCards = auctions.map(({ auction, item }, i) => (
        <AuctionCard key={i} auction={auction} item={item} />
    ));

    if (auctionCards.length == 0) {
        auctionCards = Array.from(Array(10)).fill(<ItemSkeleton />);
    }

    return (
        <div>
            <h1>Auctions</h1>
            <h3>Live Auctions</h3>
            <Row xs={1} md={3} className="g-4">
                {auctionCards}
            </Row>

            <h3>Upcoming Auctions</h3>
        </div>
    );
};

export default Auctions;
