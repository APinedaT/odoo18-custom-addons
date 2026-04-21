import { Dialog } from "@web/core/dialog/dialog";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";

export class QuotationScreen extends Component {
    static template = "pi_pos_receipt_custom.QuotationScreen";
    static components = { OrderReceipt, Dialog };
    static props = {
        close: Function,
    };
    setup() {
        this.pos = usePos();
        this.printer = useState(useService("printer"));
        this.renderer = useService("renderer");
    }
    async print() {
        await this.pos.printReceipt({
            printBillActionTriggered: true,
        });
    }
    async downloadImage() {
        const imageBase64 = await this.renderer.toJpeg(
            OrderReceipt,
            {
                data: {
                    ...this.pos.orderExportForPrinting(this.pos.get_order()),
                    isBill: true,
                    isQuotation: true,
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
        a.download = `cotizacion_${this.pos.get_order().name}.jpg`;
        a.click();
        URL.revokeObjectURL(url);
    }
}
