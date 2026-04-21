import { BillScreen } from "@pos_restaurant/app/bill_screen/bill_screen";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(BillScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.renderer = useService("renderer");
    },
    async downloadImage() {
        const imageBase64 = await this.renderer.toJpeg(
            OrderReceipt,
            {
                data: {
                    ...this.pos.orderExportForPrinting(this.pos.get_order()),
                    isBill: true,
                    show_change: false,
                },
                formatCurrency: this.env.utils.formatCurrency,
            },
            { addClass: "pos-receipt-print p-3" }
        );
        const blob = new Blob(
            [Uint8Array.from(atob(imageBase64), (c) => c.charCodeAt(0))],
            { type: "image/jpeg" }
        );
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `cuenta_${this.pos.get_order().name}.jpg`;
        a.click();
        URL.revokeObjectURL(url);
    },
});
