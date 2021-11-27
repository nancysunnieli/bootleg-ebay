import { useEffect, useState } from "react";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import { useDispatch, useSelector } from "react-redux";
import { useRouteMatch } from "react-router-dom";
import { getCurrentAuctions } from "../../slices/auctions";
import ItemSkeleton from "../Items/ItemSkeleton";
import AuctionCard from "./AuctionsCard";
const Auctions = () => {
    const { auctions } = useSelector((state) => state.auctions);
    const { cartItems } = useSelector((state) => state.cart);
    const { user } = useSelector((state) => state.auth);
    const { path } = useRouteMatch();
    const [isSortedDesc, setIsSortedDesc] = useState(true);

    const dispatch = useDispatch();
    const getAuctions = () => {
        dispatch(getCurrentAuctions());
    };

    useEffect(() => {
        getAuctions();
    }, []);

    let _auctions = [...auctions];
    if (isSortedDesc) {
        _auctions.sort((a, b) => a.auction.end_time - b.auction.end_time);
    }

    let auctionCards = _auctions.map(({ auction, item }, i) => {
        let isBuyNowDisabled =
            cartItems.findIndex((c) => c.item._id === item._id) != -1 ||
            auction.buy_now === "False" ||
            auction.buy_now === false;
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

    return (
        <div>
            <div>
                <h1>Auctions</h1>
                <Row>
                    <Col md="auto">
                        <h3>Live Auctions</h3>
                    </Col>
                    {user.is_admin ? (
                        <Col md="auto">
                            <Button onClick={() => setIsSortedDesc(!isSortedDesc)}>
                                View {isSortedDesc ? "Unsorted" : "Sorted"}
                            </Button>
                        </Col>
                    ) : null}
                </Row>
                <br />
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
