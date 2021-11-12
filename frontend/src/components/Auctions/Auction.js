import { useEffect } from "react";
import Container from "react-bootstrap/Container";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { clearAuction, getAuction } from "../../slices/auctions";
import Loading from "../Loading/Loading";
import NotFound from "../NotFound/NotFound";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Image from "react-bootstrap/Image";
import Table from "react-bootstrap/Table";

export default function Auction() {
    const { auction_id } = useParams();
    const dispatch = useDispatch();
    const { auction, getAuctionLoading } = useSelector((state) => state.auctions);

    useEffect(() => {
        dispatch(getAuction({ auction_id }));

        return () => {
            dispatch(clearAuction());
        };
    }, []);

    if (getAuctionLoading) {
        return <Loading />;
    }

    if (auction == null) {
        return <NotFound />;
    }

    const { bids, end_time, item_id, seller_id, start_time } = auction.auction;
    const { _id, category, description, isFlagged, name, photos, price, sellerID, watchlist } =
        auction.item;

    console.log("bids", bids);
    const tbody = bids.map((bid) => (
        <tr>
            <td>{bid.buyer_id}</td>
            <td>{bid.price}</td>
            <td>{new Date(bid.bid_time * 1000).toLocaleString()}</td>
        </tr>
    ));

    return (
        <div>
            <Container style={{ width: "80%" }}>
                <Row>
                    <Col>
                        <Image
                            src="https://picsum.photos/1000"
                            style={{
                                width: "30em",
                                height: "auto",
                                display: "block",
                            }}
                        />
                    </Col>
                    <Col>
                        <h1>{name}</h1>
                        <h4>{description}</h4>
                        <h5>Max bid: $49.99</h5>
                        <h5>Buy Now Price: {price}</h5>
                        <h5>{category.join(", ")}</h5>
                    </Col>
                </Row>
                <br />
                <Row>
                    <Table striped hover responsive="sm">
                        <thead>
                            <tr>
                                <th>Bidder</th>
                                <th>Bid Price</th>
                                <th>Timestamp</th>
                            </tr>
                        </thead>
                        <tbody>{tbody}</tbody>
                    </Table>
                </Row>
            </Container>
        </div>
    );
}
