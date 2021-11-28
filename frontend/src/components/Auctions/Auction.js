import { useCallback, useEffect, useState } from "react";
import Container from "react-bootstrap/Container";
import { useDispatch, useSelector } from "react-redux";
import { useHistory, useParams } from "react-router-dom";
import { clearAuction, createBid, getAuction, getAuctionBids } from "../../slices/auctions";
import Loading from "../Loading/Loading";
import NotFound from "../NotFound/NotFound";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Image from "react-bootstrap/Image";
import Table from "react-bootstrap/Table";
import Button from "react-bootstrap/Button";
import useInterval from "../../hooks/useInterval";
import moment from "moment";
import Form from "react-bootstrap/Form";
import Badge from "react-bootstrap/Badge";
import { addItemToCart } from "../../slices/cart";
import ProgressBar from "react-bootstrap/ProgressBar";
import "./Auction.css";
import EditAuctionModal from "./EditAuctionModal";
import { setEditModalVisible } from "../../slices/profile";
export default function Auction() {
    const { auction_id } = useParams();
    const dispatch = useDispatch();
    const { cartItems } = useSelector((state) => state.cart);
    const { auction, getAuctionLoading } = useSelector((state) => state.auctions);
    const { user } = useSelector((state) => state.auth);
    const [showEditAuctionModal, setEditAuctionModalVisible] = useState(false);
    const [timeNow, setTimeNow] = useState(new Date());
    const [bidAmount, setBidAmount] = useState("");
    const history = useHistory();
    const [progress, setProgressBar] = useState(0);

    const _getAuction = useCallback(() => {
        dispatch(getAuction({ auction_id }));
    }, [dispatch, auction_id]);

    const _getAuctionBids = useCallback(() => {
        dispatch(getAuctionBids({ auction_id }));
    }, [dispatch, auction_id]);

    const placeBid = useCallback(() => {
        console.log("placing bid");
        dispatch(createBid({ buyer_id: user.user_id, auction_id, price: bidAmount }));
    }, [dispatch, bidAmount, user, auction_id]);

    const buyNow = useCallback(() => {
        dispatch(addItemToCart({ item: auction.item, user_id: user.user_id }));
    }, [dispatch, auction, user]);

    useInterval(() => {
        setTimeNow(new Date());
        setProgressBar((progress + 10) % 100);
    }, 1000);

    useInterval(() => {
        if (auction == null) return;
        _getAuctionBids();
    }, 10 * 1000);

    useEffect(() => {
        _getAuction();

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

    const {
        bids,
        end_time,
        item_id,
        seller_id,
        seller_username,
        seller_rating,
        start_time,
        buy_now,
        buy_now_price,
        starting_price,
        shipping,
    } = auction.auction;
    const { _id, category, description, isFlagged, name, photos, sellerID, watchlist } =
        auction.item;

    let isSeller = false;
    if (seller_id == user.user_id) {
        isSeller = true;
    }

    const isBuyNowDisabled = buy_now === "False" || buy_now === false;
    const itemIsInCart = cartItems.findIndex((c) => c.item._id === auction.item._id) != -1;

    let isStarted = start_time * 1000 < new Date().getTime();
    let timeToStart = moment(start_time * 1000).fromNow();
    let remainingDuration = Math.min(end_time * 1000 - timeNow.getTime());
    let isEnded = end_time * 1000 < new Date().getTime();
    let timeRemaining = moment.utc(remainingDuration).format("D [days,] HH:mm:ss");

    const tbody = bids.map((bid, i) => (
        <tr key={i}>
            <td>{bid.buyer_username}</td>
            <td>${bid.price}</td>
            <td>{new Date(bid.bid_time * 1000).toLocaleString()}</td>
        </tr>
    ));

    let maxBid = 0;
    if (bids.length) {
        maxBid = Math.max(...bids.map((bid) => bid.price)) || 0;
    }

    const handleEndAuctionEarly = () => {
        window.alert("TODO");
    };

    const getActionBody = () => (
        <div>
            {isStarted ? (
                <div>
                    <h5>
                        Auction Ends In: <span style={{ color: "red" }}>{timeRemaining}</span>
                    </h5>
                    <Row>
                        <Col className={"my-auto"}>
                            <h5>
                                {isBuyNowDisabled || itemIsInCart
                                    ? "Unavailable for Buy Now"
                                    : `Buy Now Price: ${buy_now_price}`}
                            </h5>
                        </Col>
                        <Col>
                            <Button
                                size="lg"
                                variant="success"
                                onClick={buyNow}
                                disabled={isBuyNowDisabled || itemIsInCart}
                            >
                                Buy Now
                            </Button>
                        </Col>
                    </Row>
                    <h5>Current bid: ${maxBid}</h5>
                    <h5>Starting bid price: ${starting_price}</h5>

                    <Row>
                        <Col className={"my-auto"}>
                            <Form
                                onSubmit={(e) => {
                                    e.preventDefault();
                                    placeBid();
                                    setBidAmount("");
                                }}
                            >
                                <Form.Control
                                    placeholder="Enter new bid"
                                    value={bidAmount}
                                    onChange={(event) => {
                                        setBidAmount(event.target.value);
                                    }}
                                />
                            </Form>
                        </Col>
                        <Col>
                            <Button
                                size="lg"
                                onClick={placeBid}
                                disabled={bidAmount.length === 0 || itemIsInCart}
                            >
                                Place Bid
                            </Button>
                        </Col>
                    </Row>
                </div>
            ) : (
                <h5>Auction Starts: {timeToStart}</h5>
            )}
        </div>
    );

    const goToItem = () => {
        history.push(`/items/${item_id}`);
    };

    return (
        <div>
            <Container style={{ width: "80%", marginBottom: "2rem" }}>
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
                        <h1 onClick={goToItem} className="title">
                            {name}
                        </h1>
                        <h4>{description}</h4>
                        <h5>Shipping fee ${shipping}</h5>
                        <h6>
                            Sold by {seller_username} {seller_rating}★
                        </h6>

                        <Row>
                            {category.map((c, i) => (
                                <Col md="auto" key={i}>
                                    <Badge key={i} bg="primary">
                                        {c}
                                    </Badge>
                                </Col>
                            ))}
                        </Row>
                        {isSeller && (
                            <div>
                                <br />
                                <Row>
                                    <Button
                                        variant="info"
                                        onClick={() => setEditAuctionModalVisible(true)}
                                    >
                                        Edit
                                    </Button>
                                </Row>
                                <br />
                            </div>
                        )}
                        {user.is_admin === 1 && (
                            <div>
                                <br />
                                <Row>
                                    <Button
                                        variant="warning"
                                        onClick={() => handleEndAuctionEarly()}
                                    >
                                        End Auction Early
                                    </Button>
                                </Row>
                                <br />
                            </div>
                        )}
                        {isEnded ? <h5>This auction has ended</h5> : getActionBody()}
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
                <Row>
                    <p>Updates in..</p>
                </Row>
                <ProgressBar animated now={progress} />
            </Container>
            <EditAuctionModal
                show={showEditAuctionModal}
                handleClose={() => setEditAuctionModalVisible(false)}
            />
        </div>
    );
}
